#!/bin/bash

# ========================================
# Script de Build et Push des Images Docker
# ========================================

set -e

# Configuration
REGISTRY="${DOCKER_REGISTRY:-yourusername}"
VERSION="${VERSION:-latest}"

echo "🐳 Building Docker images for Kubernetes deployment..."
echo "Registry: $REGISTRY"
echo "Version: $VERSION"
echo ""

# Build Django API
echo "📦 Building Django API..."
cd django_app
docker build -f Dockerfile.prod -t $REGISTRY/django-api:$VERSION -t $REGISTRY/django-api:latest .
echo "✅ Django API built successfully"
cd ..

# Build Angular Frontend
echo "📦 Building Angular Frontend..."
cd angular-app
docker build -t $REGISTRY/angular-frontend:$VERSION -t $REGISTRY/angular-frontend:latest .
echo "✅ Angular Frontend built successfully"
cd ..

# Build Logstash
echo "📦 Building Logstash..."
cd logstash
docker build -t $REGISTRY/logstash-iot:$VERSION -t $REGISTRY/logstash-iot:latest .
echo "✅ Logstash built successfully"
cd ..

echo ""
echo "🚀 Pushing images to registry..."

# Push images
docker push $REGISTRY/django-api:$VERSION
docker push $REGISTRY/django-api:latest

docker push $REGISTRY/angular-frontend:$VERSION
docker push $REGISTRY/angular-frontend:latest

docker push $REGISTRY/logstash-iot:$VERSION
docker push $REGISTRY/logstash-iot:latest

echo ""
echo "✅ All images built and pushed successfully!"
echo ""
echo "Images:"
echo "  - $REGISTRY/django-api:$VERSION"
echo "  - $REGISTRY/angular-frontend:$VERSION"
echo "  - $REGISTRY/logstash-iot:$VERSION"
echo ""
echo "Next steps:"
echo "  1. Update k8s manifests with your registry: sed -i 's/<YOUR_REGISTRY>/$REGISTRY/g' k8s/*.yaml"
echo "  2. Deploy to Kubernetes: kubectl apply -f k8s/"
