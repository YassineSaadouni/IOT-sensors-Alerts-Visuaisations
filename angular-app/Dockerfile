# ================================
# Angular Frontend Dockerfile
# Stage 1: Build
# ================================

FROM node:18-alpine AS builder

WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm ci --silent

# Copier le code source
COPY . .

# Build de l'application Angular en mode production
RUN npm run build -- --configuration production

# ================================
# Stage 2: Production avec Nginx
# ================================

FROM nginx:alpine

LABEL maintainer="Projet Big Data IoT"
LABEL description="Angular Frontend avec Nginx"

# Copier les fichiers buildés depuis le stage builder
COPY --from=builder /app/dist/angular-app /usr/share/nginx/html

# Copier la configuration Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]
