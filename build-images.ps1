# ========================================
# Script PowerShell de Build et Push des Images Docker
# ========================================

param(
    [string]$Registry = $env:DOCKER_REGISTRY,
    [string]$Version = "latest"
)

if ([string]::IsNullOrEmpty($Registry)) {
    $Registry = Read-Host "Enter your Docker registry username"
}

Write-Host "🐳 Building Docker images for Kubernetes deployment..." -ForegroundColor Cyan
Write-Host "Registry: $Registry" -ForegroundColor Yellow
Write-Host "Version: $Version" -ForegroundColor Yellow
Write-Host ""

# Build Django API
Write-Host "📦 Building Django API..." -ForegroundColor Green
Set-Location django_app
docker build -f Dockerfile.prod -t "${Registry}/django-api:${Version}" -t "${Registry}/django-api:latest" .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "✅ Django API built successfully" -ForegroundColor Green
Set-Location ..

# Build Angular Frontend
Write-Host "📦 Building Angular Frontend..." -ForegroundColor Green
Set-Location angular-app
docker build -t "${Registry}/angular-frontend:${Version}" -t "${Registry}/angular-frontend:latest" .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "✅ Angular Frontend built successfully" -ForegroundColor Green
Set-Location ..

# Build Logstash
Write-Host "📦 Building Logstash..." -ForegroundColor Green
Set-Location logstash
docker build -t "${Registry}/logstash-iot:${Version}" -t "${Registry}/logstash-iot:latest" .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "✅ Logstash built successfully" -ForegroundColor Green
Set-Location ..

Write-Host ""
Write-Host "🚀 Pushing images to registry..." -ForegroundColor Cyan

# Push images
docker push "${Registry}/django-api:${Version}"
docker push "${Registry}/django-api:latest"

docker push "${Registry}/angular-frontend:${Version}"
docker push "${Registry}/angular-frontend:latest"

docker push "${Registry}/logstash-iot:${Version}"
docker push "${Registry}/logstash-iot:latest"

Write-Host ""
Write-Host "✅ All images built and pushed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Images:" -ForegroundColor Yellow
Write-Host "  - ${Registry}/django-api:${Version}"
Write-Host "  - ${Registry}/angular-frontend:${Version}"
Write-Host "  - ${Registry}/logstash-iot:${Version}"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Update k8s manifests with your registry:"
Write-Host "     Get-ChildItem k8s/*.yaml | ForEach-Object { (Get-Content `$_) -replace '<YOUR_REGISTRY>', '$Registry' | Set-Content `$_ }"
Write-Host "  2. Deploy to Kubernetes: kubectl apply -f k8s/"
