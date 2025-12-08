#!/bin/bash
cd "$(dirname "$0")/angular-app"
echo "Installation des dépendances npm..."
npm install --legacy-peer-deps
echo ""
echo "Démarrage de l'application Angular..."
npm start
