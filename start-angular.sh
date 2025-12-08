#!/bin/bash

# Script d'installation et de lancement de l'application Angular

echo "🚀 Installation de l'application Angular IoT Dashboard"
echo "======================================================="
echo ""

# Vérifier que Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Veuillez installer Node.js d'abord."
    echo "   Téléchargez Node.js depuis: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ NPM version: $(npm --version)"
echo ""

# Se déplacer dans le dossier angular-app
cd "$(dirname "$0")/angular-app"

# Vérifier si node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances npm..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de l'installation des dépendances"
        exit 1
    fi
    echo "✅ Dépendances installées avec succès"
else
    echo "✅ Les dépendances sont déjà installées"
fi

echo ""
echo "🔧 Configuration de l'environnement..."
echo "   API URL: http://localhost:8000/api"
echo "   Upload URL: http://localhost:8000/upload"
echo ""

# Vérifier que le backend Django tourne
echo "🔍 Vérification du backend Django..."
if curl -s http://localhost:8000/api/health/ > /dev/null 2>&1; then
    echo "✅ Backend Django accessible"
else
    echo "⚠️  Backend Django non accessible"
    echo "   Assurez-vous que le backend tourne avec: docker-compose up -d"
fi

echo ""
echo "🚀 Démarrage de l'application Angular..."
echo "   L'application sera accessible sur: http://localhost:4200"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Démarrer l'application
npm start
