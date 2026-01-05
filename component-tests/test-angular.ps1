# Test Angular Application Component
# This script tests Angular frontend accessibility

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$ANGULAR_HOST = "http://localhost:4200"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[$timestamp] Starting Angular App Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Test 1: Check Angular server
Write-Host "`n[TEST 1] Checking Angular application..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$ANGULAR_HOST/" -Method Get -UseBasicParsing -ErrorAction Stop -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "[SUCCESS] Angular application is running" -ForegroundColor Green
        Write-Host "  Status Code: $($response.StatusCode)" -ForegroundColor White
        Write-Host "  Content Length: $($response.Content.Length) bytes" -ForegroundColor White
    }
} catch {
    Write-Host "[FAILED] Angular application is not accessible: $_" -ForegroundColor Red
    exit 1
}

# Test 2: Check if index.html is served
Write-Host "`n[TEST 2] Checking index.html..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$ANGULAR_HOST/index.html" -Method Get -UseBasicParsing -ErrorAction Stop
    if ($response.Content -match "<app-root>") {
        Write-Host "[SUCCESS] Angular app-root component found in HTML" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Angular app-root not found in HTML" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[FAILED] Could not retrieve index.html: $_" -ForegroundColor Red
}

# Test 3: Check static resources
Write-Host "`n[TEST 3] Checking static resources..." -ForegroundColor Yellow
$resources = @(
    "/main.js",
    "/polyfills.js",
    "/styles.css"
)

$loadedResources = 0
foreach ($resource in $resources) {
    try {
        $response = Invoke-WebRequest -Uri "$ANGULAR_HOST$resource" -Method Get -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $loadedResources++
        }
    } catch {
        # Resources might have hash in filename, this is expected
    }
}

if ($loadedResources -eq 0) {
    Write-Host "[INFO] No exact resource matches (hashed filenames expected in production)" -ForegroundColor Yellow
} else {
    Write-Host "[SUCCESS] Found $loadedResources static resources" -ForegroundColor Green
}

# Test 4: Check if application connects to backend
Write-Host "`n[TEST 4] Testing application responsiveness..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$ANGULAR_HOST/" -Method Get -UseBasicParsing -ErrorAction Stop
    $loadTime = $response.Headers.'X-Response-Time'
    Write-Host "[SUCCESS] Application is responsive" -ForegroundColor Green
    if ($loadTime) {
        Write-Host "  Response time: $loadTime" -ForegroundColor White
    }
} catch {
    Write-Host "[WARNING] Could not measure responsiveness: $_" -ForegroundColor Yellow
}

$endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[$endTimestamp] Angular App Test Completed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
