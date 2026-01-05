# Test Kibana Component
# This script tests Kibana connectivity and status

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$KIBANA_HOST = "http://localhost:5601"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[$timestamp] Starting Kibana Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Test 1: Check Kibana status
Write-Host "`n[TEST 1] Checking Kibana status..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$KIBANA_HOST/api/status" -Method Get -ErrorAction Stop
    Write-Host "[SUCCESS] Kibana is running" -ForegroundColor Green
    Write-Host "  Status: $($response.status.overall.state)" -ForegroundColor White
    Write-Host "  Version: $($response.version.number)" -ForegroundColor White
} catch {
    Write-Host "[FAILED] Kibana is not accessible: $_" -ForegroundColor Red
    exit 1
}

# Test 2: Check Kibana connectivity to Elasticsearch
Write-Host "`n[TEST 2] Checking Kibana-Elasticsearch connection..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$KIBANA_HOST/api/status" -Method Get -ErrorAction Stop
    if ($response.status.statuses) {
        $esStatus = $response.status.statuses | Where-Object { $_.id -eq 'elasticsearch' }
        if ($esStatus) {
            Write-Host "[SUCCESS] Kibana is connected to Elasticsearch" -ForegroundColor Green
            Write-Host "  ES Status: $($esStatus.state)" -ForegroundColor White
        }
    }
} catch {
    Write-Host "[FAILED] Could not check ES connection: $_" -ForegroundColor Red
}

# Test 3: Test Kibana homepage accessibility
Write-Host "`n[TEST 3] Testing Kibana web interface..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$KIBANA_HOST/app/home" -Method Get -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "[SUCCESS] Kibana web interface is accessible" -ForegroundColor Green
    }
} catch {
    Write-Host "[WARNING] Kibana web interface check failed: $_" -ForegroundColor Yellow
}

$endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[$endTimestamp] Kibana Test Completed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
