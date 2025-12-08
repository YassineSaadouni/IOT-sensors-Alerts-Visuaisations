"""
Service layer pour interagir avec Elasticsearch
"""
import logging
from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch
from django.conf import settings

logger = logging.getLogger(__name__)


class ElasticsearchService:
    """Service pour gérer les opérations Elasticsearch"""
    
    def __init__(self):
        self.es = Elasticsearch([settings.ELASTICSEARCH_URL])
        self.default_index = settings.ELASTICSEARCH_INDEX['IOT_DATA']
    
    def check_connection(self) -> bool:
        """Vérifier la connexion à Elasticsearch"""
        try:
            return self.es.ping()
        except Exception as e:
            logger.error(f"Erreur connexion Elasticsearch: {e}")
            return False
    
    def get_indices(self) -> List[str]:
        """Obtenir la liste des indices"""
        try:
            indices = self.es.cat.indices(format='json')
            return [idx['index'] for idx in indices]
        except Exception as e:
            logger.error(f"Erreur récupération indices: {e}")
            return []
    
    def count_documents(self, index: str = None) -> int:
        """Compter les documents dans un index"""
        try:
            index = index or self.default_index
            result = self.es.count(index=index)
            return result['count']
        except Exception as e:
            logger.error(f"Erreur comptage documents: {e}")
            return 0
    
    def search(
        self,
        query: Optional[str] = None,
        index: str = None,
        size: int = 50,
        from_offset: int = 0,
        filters: Optional[Dict] = None,
        sort_by: str = '@timestamp',
        sort_order: str = 'desc'
    ) -> Dict[str, Any]:
        """
        Rechercher des documents avec filtres et tri
        
        Args:
            query: Texte de recherche
            index: Nom de l'index
            size: Nombre de résultats
            from_offset: Offset pour pagination
            filters: Filtres additionnels (dict)
            sort_by: Champ de tri
            sort_order: Ordre (asc/desc)
        
        Returns:
            Dict contenant les résultats et métadonnées
        """
        try:
            index = index or self.default_index
            
            # Construction de la requête
            body = {
                "query": self._build_query(query, filters),
                "size": size,
                "from": from_offset,
                "sort": [{sort_by: {"order": sort_order}}]
            }
            
            logger.info(f"Recherche Elasticsearch: index={index}, query={query}, filters={filters}")
            
            result = self.es.search(index=index, body=body)
            
            # Extraire les résultats
            hits = result['hits']['hits']
            total = result['hits']['total']['value']
            
            documents = [
                {
                    '_id': hit['_id'],
                    '_score': hit.get('_score'),
                    **hit['_source']
                }
                for hit in hits
            ]
            
            return {
                'total': total,
                'count': len(documents),
                'documents': documents,
                'from': from_offset,
                'size': size
            }
            
        except Exception as e:
            logger.error(f"Erreur recherche Elasticsearch: {e}")
            return {
                'total': 0,
                'count': 0,
                'documents': [],
                'error': str(e)
            }
    
    def _build_query(self, query: Optional[str], filters: Optional[Dict]) -> Dict:
        """Construire la requête Elasticsearch"""
        
        # Requête de base
        must_clauses = []
        filter_clauses = []
        
        # Recherche textuelle
        if query:
            must_clauses.append({
                "multi_match": {
                    "query": query,
                    "fields": ["*"],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })
        
        # Appliquer les filtres
        if filters:
            for field, value in filters.items():
                if value is not None and value != '':
                    if field.endswith('_from'):
                        # Date range from
                        actual_field = field.replace('_from', '')
                        filter_clauses.append({
                            "range": {
                                actual_field: {"gte": value}
                            }
                        })
                    elif field.endswith('_to'):
                        # Date range to
                        actual_field = field.replace('_to', '')
                        filter_clauses.append({
                            "range": {
                                actual_field: {"lte": value}
                            }
                        })
                    else:
                        # Match exact
                        filter_clauses.append({
                            "term": {
                                f"{field}.keyword": value
                            }
                        })
        
        # Construire la requête finale
        if must_clauses or filter_clauses:
            return {
                "bool": {
                    "must": must_clauses if must_clauses else [{"match_all": {}}],
                    "filter": filter_clauses
                }
            }
        else:
            return {"match_all": {}}
    
    def get_by_id(self, doc_id: str, index: str = None) -> Optional[Dict]:
        """Récupérer un document par son ID"""
        try:
            index = index or self.default_index
            result = self.es.get(index=index, id=doc_id)
            return {
                '_id': result['_id'],
                **result['_source']
            }
        except Exception as e:
            logger.error(f"Erreur récupération document {doc_id}: {e}")
            return None
    
    def aggregate(
        self,
        field: str,
        agg_type: str = 'terms',
        index: str = None,
        size: int = 10,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Effectuer une agrégation
        
        Args:
            field: Champ à agréger
            agg_type: Type d'agrégation (terms, stats, date_histogram, range)
            index: Nom de l'index
            size: Nombre de buckets (pour terms)
            **kwargs: Paramètres additionnels
        
        Returns:
            Résultats de l'agrégation
        """
        try:
            index = index or self.default_index
            
            # Construire l'agrégation
            if agg_type == 'terms':
                agg_body = {
                    "terms": {
                        "field": f"{field}.keyword" if not field.endswith('.keyword') else field,
                        "size": size
                    }
                }
            elif agg_type == 'stats':
                agg_body = {
                    "stats": {
                        "field": field
                    }
                }
            elif agg_type == 'date_histogram':
                interval = kwargs.get('interval', '1d')
                agg_body = {
                    "date_histogram": {
                        "field": field,
                        "calendar_interval": interval
                    }
                }
            elif agg_type == 'range':
                ranges = kwargs.get('ranges', [])
                agg_body = {
                    "range": {
                        "field": field,
                        "ranges": ranges
                    }
                }
            else:
                raise ValueError(f"Type d'agrégation non supporté: {agg_type}")
            
            body = {
                "size": 0,
                "aggs": {
                    "result": agg_body
                }
            }
            
            result = self.es.search(index=index, body=body)
            
            return {
                'aggregation_type': agg_type,
                'field': field,
                'result': result['aggregations']['result']
            }
            
        except Exception as e:
            logger.error(f"Erreur agrégation: {e}")
            return {
                'error': str(e)
            }
    
    def get_statistics(self, index: str = None) -> Dict[str, Any]:
        """Obtenir des statistiques globales"""
        try:
            index = index or self.default_index
            
            # Compter les documents
            total_docs = self.count_documents(index)
            
            # Agrégations multiples
            body = {
                "size": 0,
                "aggs": {
                    "by_file_type": {
                        "terms": {"field": "file_type.keyword", "size": 10}
                    },
                    "by_source_file": {
                        "terms": {"field": "source_file.keyword", "size": 20}
                    },
                    "by_status": {
                        "terms": {"field": "status.keyword", "size": 10}
                    },
                    "upload_timeline": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "calendar_interval": "1d"
                        }
                    }
                }
            }
            
            result = self.es.search(index=index, body=body)
            aggs = result['aggregations']
            
            return {
                'total_documents': total_docs,
                'by_file_type': [
                    {'key': b['key'], 'count': b['doc_count']}
                    for b in aggs['by_file_type']['buckets']
                ],
                'by_source_file': [
                    {'key': b['key'], 'count': b['doc_count']}
                    for b in aggs['by_source_file']['buckets']
                ],
                'by_status': [
                    {'key': b['key'], 'count': b['doc_count']}
                    for b in aggs.get('by_status', {}).get('buckets', [])
                ],
                'upload_timeline': [
                    {
                        'date': b['key_as_string'],
                        'count': b['doc_count']
                    }
                    for b in aggs['upload_timeline']['buckets']
                ]
            }
            
        except Exception as e:
            logger.error(f"Erreur statistiques: {e}")
            return {'error': str(e)}
    
    def get_alertes_statistics(self) -> Dict[str, Any]:
        """Statistiques pour les alertes"""
        try:
            body = {
                "size": 0,
                "aggs": {
                    "by_severite": {"terms": {"field": "severite.keyword"}},
                    "by_statut": {"terms": {"field": "statut.keyword"}},
                    "by_categorie": {"terms": {"field": "categorie.keyword"}},
                    "by_batiment": {"terms": {"field": "batiment.keyword"}},
                    "count_non_resolue": {
                        "filter": {"term": {"statut.keyword": "non_resolue"}}
                    }
                }
            }
            result = self.es.search(index="iot-alertes", body=body)
            aggs = result['aggregations']
            
            return {
                'total': self.count_documents("iot-alertes"),
                'by_severite': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_severite']['buckets']],
                'by_statut': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_statut']['buckets']],
                'by_categorie': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_categorie']['buckets']],
                'by_batiment': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_batiment']['buckets']],
                'non_resolues': aggs['count_non_resolue']['doc_count']
            }
        except Exception as e:
            logger.error(f"Erreur stats alertes: {e}")
            return {'error': str(e)}
    
    def get_capteurs_statistics(self) -> Dict[str, Any]:
        """Statistiques pour les capteurs"""
        try:
            body = {
                "size": 0,
                "aggs": {
                    "by_type": {"terms": {"field": "type.keyword"}},
                    "by_statut": {"terms": {"field": "statut_capteur.keyword"}},
                    "by_batiment": {"terms": {"field": "batiment.keyword"}},
                    "batterie_stats": {"stats": {"field": "batterie"}},
                    "valeur_stats": {"stats": {"field": "valeur"}}
                }
            }
            result = self.es.search(index="iot-capteurs", body=body)
            aggs = result['aggregations']
            
            return {
                'total': self.count_documents("iot-capteurs"),
                'by_type': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_type']['buckets']],
                'by_statut': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_statut']['buckets']],
                'by_batiment': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_batiment']['buckets']],
                'batterie_stats': aggs['batterie_stats'],
                'valeur_stats': aggs['valeur_stats']
            }
        except Exception as e:
            logger.error(f"Erreur stats capteurs: {e}")
            return {'error': str(e)}
    
    def get_consommation_statistics(self) -> Dict[str, Any]:
        """Statistiques pour la consommation"""
        try:
            body = {
                "size": 0,
                "aggs": {
                    "by_type_energie": {"terms": {"field": "type_energie.keyword"}},
                    "by_sous_type": {"terms": {"field": "sous_type.keyword"}},
                    "by_batiment": {"terms": {"field": "batiment.keyword"}},
                    "consommation_stats": {"stats": {"field": "valeur_consommation"}},
                    "cout_total": {"sum": {"field": "cout_estime"}},
                    "empreinte_carbone_total": {"sum": {"field": "empreinte_carbone"}}
                }
            }
            result = self.es.search(index="iot-consommation", body=body)
            aggs = result['aggregations']
            
            return {
                'total': self.count_documents("iot-consommation"),
                'by_type_energie': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_type_energie']['buckets']],
                'by_sous_type': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_sous_type']['buckets']],
                'by_batiment': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_batiment']['buckets']],
                'consommation_stats': aggs['consommation_stats'],
                'cout_total': aggs['cout_total']['value'],
                'empreinte_carbone_total': aggs['empreinte_carbone_total']['value']
            }
        except Exception as e:
            logger.error(f"Erreur stats consommation: {e}")
            return {'error': str(e)}
    
    def get_occupation_statistics(self) -> Dict[str, Any]:
        """Statistiques pour l'occupation"""
        try:
            body = {
                "size": 0,
                "aggs": {
                    "by_type_salle": {"terms": {"field": "type_salle.keyword"}},
                    "by_statut": {"terms": {"field": "statut_occupation.keyword"}},
                    "by_batiment": {"terms": {"field": "batiment.keyword"}},
                    "taux_occupation_moyen": {"avg": {"script": {
                        "source": "doc['nombre_personnes'].value / doc['capacite_max'].value * 100"
                    }}},
                    "personnes_total": {"sum": {"field": "nombre_personnes"}}
                }
            }
            result = self.es.search(index="iot-occupation", body=body)
            aggs = result['aggregations']
            
            return {
                'total': self.count_documents("iot-occupation"),
                'by_type_salle': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_type_salle']['buckets']],
                'by_statut': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_statut']['buckets']],
                'by_batiment': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_batiment']['buckets']],
                'taux_occupation_moyen': aggs['taux_occupation_moyen']['value'],
                'personnes_total': aggs['personnes_total']['value']
            }
        except Exception as e:
            logger.error(f"Erreur stats occupation: {e}")
            return {'error': str(e)}
    
    def get_maintenance_statistics(self) -> Dict[str, Any]:
        """Statistiques pour la maintenance"""
        try:
            body = {
                "size": 0,
                "aggs": {
                    "by_type_equipement": {"terms": {"field": "type_equipement.keyword"}},
                    "by_type_maintenance": {"terms": {"field": "type_maintenance.keyword"}},
                    "by_severite": {"terms": {"field": "severite.keyword"}},
                    "by_batiment": {"terms": {"field": "batiment.keyword"}},
                    "cout_total": {"sum": {"field": "cout_estime"}},
                    "vie_restante_stats": {"stats": {"field": "vie_restante"}},
                    "duree_moyenne": {"avg": {"field": "duree_intervention_estimee"}}
                }
            }
            result = self.es.search(index="iot-maintenance", body=body)
            aggs = result['aggregations']
            
            return {
                'total': self.count_documents("iot-maintenance"),
                'by_type_equipement': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_type_equipement']['buckets']],
                'by_type_maintenance': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_type_maintenance']['buckets']],
                'by_severite': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_severite']['buckets']],
                'by_batiment': [{'key': b['key'], 'count': b['doc_count']} for b in aggs['by_batiment']['buckets']],
                'cout_total': aggs['cout_total']['value'],
                'vie_restante_stats': aggs['vie_restante_stats'],
                'duree_moyenne': aggs['duree_moyenne']['value']
            }
        except Exception as e:
            logger.error(f"Erreur stats maintenance: {e}")
            return {'error': str(e)}
