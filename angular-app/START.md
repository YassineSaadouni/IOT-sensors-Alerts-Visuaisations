# 🚀 Démarrage Rapide - Instructions Simples

## ⚡ Installation et Lancement

### Étape 1: Installer les dépendances (une seule fois)

```bash
cd angular-app
npm install --legacy-peer-deps
```

**Note:** L'installation prend 2-5 minutes. Attendez que ce soit terminé!

### Étape 2: Démarrer l'application

```bash
npm start
```

L'application sera disponible sur: **http://localhost:4200**

---

## 🐛 Si vous avez des erreurs

### Erreur: "ENOTEMPTY" ou "Cannot remove directory"

**Solution Windows:**
```cmd
cd angular-app
rd /s /q node_modules
del package-lock.json
npm install --legacy-peer-deps
```

**Solution Linux/Mac:**
```bash
cd angular-app
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### Erreur: "Cannot find module"

**Solution:**
```bash
cd angular-app
npm install --legacy-peer-deps
```

### Erreur: "Port 4200 already in use"

**Solution:**
```bash
# Utilisez un autre port
ng serve --port 4201
```

---

## ✅ Vérification

Une fois démarré, vous devriez voir:
```
** Angular Live Development Server is listening on localhost:4200 **
✔ Compiled successfully.
```

Ouvrez votre navigateur sur: **http://localhost:4200**

---

## 📊 Backend requis

Assurez-vous que le backend Django tourne:
```bash
docker-compose up -d
curl http://localhost:8000/api/health/
```

---

## 🎯 Commandes Utiles

```bash
# Démarrer
npm start

# Build de production
npm run build

# Tests
npm test

# Nettoyer et réinstaller
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

**Bon développement! 🚀**
