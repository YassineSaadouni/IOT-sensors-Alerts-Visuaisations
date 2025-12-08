# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! Ce guide vous aidera à contribuer efficacement.

## 📋 Comment contribuer

### 1. Fork et Clone

```bash
# Fork le repository sur GitHub
# Puis cloner votre fork
git clone https://github.com/your-username/projet-iot.git
cd projet-iot
```

### 2. Créer une branche

```bash
# Créer une branche pour votre feature ou fix
git checkout -b feature/nom-de-votre-feature
# ou
git checkout -b fix/nom-du-bug
```

### 3. Faire vos modifications

- Suivez les conventions de code du projet
- Ajoutez des commentaires clairs
- Testez vos modifications localement

### 4. Commit et Push

```bash
# Ajouter les fichiers modifiés
git add .

# Commit avec un message descriptif
git commit -m "feat: ajout de la fonctionnalité X"

# Push vers votre fork
git push origin feature/nom-de-votre-feature
```

### 5. Créer une Pull Request

- Allez sur GitHub
- Cliquez sur "New Pull Request"
- Décrivez vos modifications en détail
- Attendez la review

## 🎯 Types de contributions

### Bugs
- Signalez les bugs via les Issues GitHub
- Incluez les étapes pour reproduire le bug
- Ajoutez les logs pertinents

### Nouvelles fonctionnalités
- Proposez d'abord via une Issue
- Discutez de l'implémentation
- Créez ensuite votre PR

### Documentation
- Améliorations du README
- Corrections de fautes
- Ajout d'exemples

### Tests
- Ajout de tests unitaires
- Tests d'intégration
- Tests de performance

## 📝 Conventions de code

### Python (Django)
```python
# Suivre PEP 8
# Noms de variables en snake_case
user_name = "example"

# Noms de classes en PascalCase
class UserService:
    pass

# Docstrings pour les fonctions
def get_user_data(user_id):
    """
    Récupère les données d'un utilisateur.
    
    Args:
        user_id (int): ID de l'utilisateur
        
    Returns:
        dict: Données de l'utilisateur
    """
    pass
```

### TypeScript (Angular)
```typescript
// Noms de variables en camelCase
const userName = 'example';

// Noms de classes en PascalCase
export class UserService {
  // Membres privés avec _
  private _userId: number;
  
  // Typage explicite
  getUserData(id: number): Observable<User> {
    // Implementation
  }
}
```

## 🔍 Standards de commit

Utilisez le format Conventional Commits :

```
<type>(<scope>): <description>

[corps optionnel]

[footer optionnel]
```

### Types
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation seulement
- `style`: Formatage, pas de changement de code
- `refactor`: Refactorisation du code
- `test`: Ajout ou modification de tests
- `chore`: Maintenance, configuration

### Exemples
```
feat(api): ajout endpoint pour les alertes critiques
fix(logstash): correction du parsing CSV des capteurs
docs(readme): mise à jour instructions d'installation
```

## ✅ Checklist avant PR

- [ ] Le code compile sans erreurs
- [ ] Tous les tests passent
- [ ] La documentation est à jour
- [ ] Les commits suivent les conventions
- [ ] Le code est formaté correctement
- [ ] Pas de console.log() ou print() de debug
- [ ] Les secrets/credentials ne sont pas commités

## 🧪 Tester localement

### Backend (Django)
```bash
# Démarrer les services
docker-compose up -d

# Tester l'API
curl http://localhost:8000/api/health

# Voir les logs
docker logs django_container -f
```

### Frontend (Angular)
```bash
cd angular-app
npm install
npm start
# Naviguer vers http://localhost:4200
```

### Tests unitaires
```bash
# Django
docker exec django_container python manage.py test

# Angular
cd angular-app
npm test
```

## 📦 Structure des PR

### Titre
Clair et descriptif : "Ajout de l'API de notifications en temps réel"

### Description
```markdown
## Description
Brève description des changements

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Comment tester
1. Démarrer Docker Compose
2. Exécuter curl http://localhost:8000/api/notifications
3. Vérifier la réponse

## Checklist
- [x] Code testé localement
- [x] Documentation mise à jour
- [x] Tests ajoutés/mis à jour
```

## 🐛 Signaler un bug

Utilisez le template suivant :

```markdown
## Description du bug
Description claire et concise

## Étapes pour reproduire
1. Aller à '...'
2. Cliquer sur '...'
3. Scroller jusqu'à '...'
4. Voir l'erreur

## Comportement attendu
Ce qui devrait se passer

## Screenshots
Si applicable

## Environnement
- OS: [e.g. Windows 11]
- Docker version: [e.g. 20.10.17]
- Navigateur: [e.g. Chrome 120]

## Logs
```
Coller les logs pertinents
```
```

## 💡 Proposer une fonctionnalité

```markdown
## Fonctionnalité proposée
Description claire de la fonctionnalité

## Problème résolu
Quel problème cette fonctionnalité résout-elle ?

## Solution proposée
Comment l'implémenter ?

## Alternatives considérées
Y a-t-il d'autres façons de faire ?

## Contexte additionnel
Toute autre information pertinente
```

## 🤝 Code de conduite

- Soyez respectueux et professionnel
- Acceptez les critiques constructives
- Concentrez-vous sur le meilleur pour le projet
- Montrez de l'empathie envers les autres contributeurs

## 📞 Questions

Si vous avez des questions :
- Ouvrez une Issue avec le label "question"
- Consultez la documentation existante
- Vérifiez les Issues/PR similaires

## 🎉 Remerciements

Merci à tous les contributeurs qui aident à améliorer ce projet !

---

**Note**: Ce projet est développé dans un cadre académique. Toutes les contributions doivent respecter les bonnes pratiques de développement et la qualité du code.
