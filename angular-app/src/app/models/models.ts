// Models pour l'application

export interface ApiResponse<T> {
  total: number;
  count: number;
  documents: T[];
  from?: number;
  size?: number;
}

export interface Device {
  _id: string;
  _score?: number;
  '@timestamp': string;
  '@version': string;
  source_file: string;
  file_type: string;
  upload_timestamp: string;
  timestamp: string;
  device_id?: string;
  vehicule_id?: string;
  capteur_id?: string;
  status?: string;
  [key: string]: any;
}

export interface Sensor extends Device {
  capteur_id: string;
  temperature?: number;
  humidity?: number;
  battery_level?: number;
  location?: string;
  status?: string;
}

export interface Vehicle extends Device {
  vehicule_id: string;
  latitude?: number;
  longitude?: number;
  vitesse?: number;
  fuel_level?: number;
  driver?: string;
  status?: string;
}

export interface Statistics {
  total_documents: number;
  by_file_type: BucketItem[];
  by_source_file: BucketItem[];
  by_status: BucketItem[];
  upload_timeline: TimelineItem[];
}

export interface BucketItem {
  key: string;
  count: number;
}

export interface TimelineItem {
  date: string;
  count: number;
}

export interface AggregationResult {
  aggregation_type: string;
  field: string;
  result: {
    buckets?: Bucket[];
    min?: number;
    max?: number;
    avg?: number;
    sum?: number;
    count?: number;
  };
}

export interface Bucket {
  key: string;
  doc_count: number;
}

export interface SearchParams {
  query?: string;
  index?: string;
  size?: number;
  from?: number;
  from_offset?: number;
  device_id?: string;
  vehicle_id?: string;
  source_file?: string;
  file_type?: string;
  status?: string;
  date_from?: string;
  date_to?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  filters?: { [key: string]: any };
  sort?: Array<{ field: string; order: 'asc' | 'desc' }>;
}

export interface HealthStatus {
  status: string;
  timestamp: string;
  services: {
    redis: string;
    elasticsearch: string;
    redis_queue_length: number;
  };
}

export interface FileUploadHistory {
  id: number;
  filename: string;
  file_type: string;
  file_size: number;
  records_count: number;
  timestamp: string;
  status: string;
  error_message?: string;
}

export interface SensorStatistics {
  total: number;
  by_status: BucketItem[];
  by_location: BucketItem[];
  temperature_stats: {
    min: number;
    max: number;
    avg: number;
  };
  humidity_stats: {
    min: number;
    max: number;
    avg: number;
  };
  battery_stats: {
    min: number;
    max: number;
    avg: number;
  };
}

export interface VehicleStatistics {
  total: number;
  by_status: BucketItem[];
  by_driver: BucketItem[];
  speed_stats: {
    min: number;
    max: number;
    avg: number;
  };
  fuel_stats: {
    min: number;
    max: number;
    avg: number;
  };
}

// === Nouveaux modèles pour les fichiers logs ===

export interface Alerte {
  _id?: string;
  id_alerte: string;
  timestamp: string;
  type_alerte: string;
  categorie: string;
  severite: string;
  priorite: string;
  capteur_id: string;
  valeur_actuelle: number;
  seuil: number;
  duree_depassement: number;
  description: string;
  batiment: string;
  salle: string;
  etage: number;
  zone: string;
  technicien_assigné: string;
  statut: string;
  date_creation: string;
  date_modification: string;
  actions_requises: string[];
  impact: string;
  code_erreur: string;
}

export interface CapteurData {
  _id?: string;
  timestamp: string;
  capteur_id: string;
  type: string;
  valeur: number;
  unite: string;
  batiment: string;
  salle: string;
  etage: number;
  zone: string;
  statut_capteur: string;
  batterie: number;
  precision: number;
  derniere_calibration: string;
  seuil_min: number;
  seuil_max: number;
}

export interface Consommation {
  _id?: string;
  timestamp: string;
  periode_mesure: string;
  type_energie: string;
  sous_type: string;
  valeur_consommation: number;
  unite: string;
  batiment: string;
  zone: string;
  equipement_id: string;
  cout_estime: number;
  cout_unitaire: number;
  empreinte_carbone: number;
  tendance: string;
  comparaison_mois_precedent: number;
  pointes_consommation: string[];
  facteur_charge: number;
}

export interface Occupation {
  _id?: string;
  timestamp: string;
  salle_id: string;
  batiment: string;
  type_salle: string;
  capacite_max: number;
  nombre_personnes: number;
  taux_utilisation: string;
  evenement: string;
  organisateur: string;
  duree_prevue: string;
  equipements_utilises: string;
  temperature_moyenne: number;
  co2_moyen: number;
  consommation_elec: number;
  statut_occupation: string;
  zone: string;
  etage: number;
}

export interface MaintenanceData {
  _id?: string;
  timestamp: string;
  intervention_id: string;
  equipement_id: string;
  type_equipement: string;
  marque: string;
  modele: string;
  type_maintenance: string;
  severite: string;
  vie_restante: number;
  prediction_panne: string;
  cout_estime: number;
  technicien: string;
  batiment: string;
  salle: string;
  zone: string;
  description: string;
  composants_affectes: string;
  historique_pannes: string;
  duree_intervention_estimee: number;
  pieces_requises: string;
}

export interface AlertesStats {
  total: number;
  by_severite: BucketItem[];
  by_statut: BucketItem[];
  by_categorie: BucketItem[];
  by_batiment: BucketItem[];
  non_resolues: number;
}

export interface CapteursStats {
  total: number;
  by_type: BucketItem[];
  by_statut: BucketItem[];
  by_batiment: BucketItem[];
  batterie_stats: StatsData;
  valeur_stats: StatsData;
}

export interface ConsommationStats {
  total: number;
  by_type_energie: BucketItem[];
  by_sous_type: BucketItem[];
  by_batiment: BucketItem[];
  consommation_stats: StatsData;
  cout_total: number;
  empreinte_carbone_total: number;
}

export interface OccupationStats {
  total: number;
  by_type_salle: BucketItem[];
  by_statut: BucketItem[];
  by_batiment: BucketItem[];
  taux_occupation_moyen: number;
  personnes_total: number;
}

export interface MaintenanceStats {
  total: number;
  by_type_equipement: BucketItem[];
  by_type_maintenance: BucketItem[];
  by_severite: BucketItem[];
  by_batiment: BucketItem[];
  cout_total: number;
  vie_restante_stats: StatsData;
  duree_moyenne: number;
}

export interface StatsData {
  count: number;
  min: number;
  max: number;
  avg: number;
  sum: number;
}
