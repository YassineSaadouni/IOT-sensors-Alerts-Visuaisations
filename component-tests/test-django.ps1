# Test Django API Component
# This script tests Django application endpoints

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$DJANGO_HOST = "http://localhost:8000"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[$timestamp] Starting Django API Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Test 1: Check Django server health
Write-Host "`n[TEST 1] Checking Django server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$DJANGO_HOST/" -Method Get -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "[SUCCESS] Django server is responding" -ForegroundColor Green
        Write-Host "  Status Code: $($response.StatusCode)" -ForegroundColor White
    }
} catch {
    Write-Host "[FAILED] Django server is not accessible: $_" -ForegroundColor Red
    exit 1
}

# Test 2: Test API endpoints
Write-Host "`n[TEST 2] Testing API endpoints..." -ForegroundColor Yellow
$endpoints = @(
    "/api/",
    "/api/health/",
    "/api/search/"
)

foreach ($endpoint in $endpoints) {
    try {
        $response = Invoke-WebRequest -Uri "$DJANGO_HOST$endpoint" -Method Get -UseBasicParsing -ErrorAction Stop
        Write-Host "[SUCCESS] Endpoint $endpoint is accessible (Status: $($response.StatusCode))" -ForegroundColor Green
    } catch {
        if ($_.Exception.Response.StatusCode.Value__ -eq 405) {
            Write-Host "[INFO] Endpoint $endpoint exists but requires different method" -ForegroundColor Yellow
        } else {
            Write-Host "[WARNING] Endpoint $endpoint: $($_.Exception.Message)" -ForegroundColor Yellow
        }
    }
}

# Test 3: Test file upload capability
Write-Host "`n[TEST 3] Testing file upload endpoint..." -ForegroundColor Yellow
try {
    $testData = @{
        test = "data"
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$DJANGO_HOST/api/upload/" -Method Post -Body $testData -ContentType "application/json" -UseBasicParsing -ErrorAction Stop
    Write-Host "[SUCCESS] Upload endpoint is accessible" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode.Value__ -eq 400 -or $_.Exception.Response.StatusCode.Value__ -eq 415) {
        Write-Host "[INFO] Upload endpoint exists (validation error expected)" -ForegroundColor Yellow
    } else {
        Write-Host "[WARNING] Upload endpoint test: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# Test 4: Check database connection
Write-Host "`n[TEST 4] Checking database connectivity..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$DJANGO_HOST/admin/" -Method Get -UseBasicParsing -ErrorAction Stop
    Write-Host "[SUCCESS] Database is accessible (admin page loads)" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Could not verify database: $_" -ForegroundColor Yellow
}

$endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[$endTimestamp] Django API Test Completed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
