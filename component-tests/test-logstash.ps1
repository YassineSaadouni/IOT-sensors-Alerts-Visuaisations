# Test Logstash Component
# This script tests Logstash connectivity and pipeline status

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$LOGSTASH_HOST = "http://localhost:9600"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[$timestamp] Starting Logstash Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Test 1: Check Logstash API health
Write-Host "`n[TEST 1] Checking Logstash health..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$LOGSTASH_HOST/" -Method Get -ErrorAction Stop
    Write-Host "[SUCCESS] Logstash is running" -ForegroundColor Green
    Write-Host "  Version: $($response.version)" -ForegroundColor White
    Write-Host "  HTTP Address: $($response.http_address)" -ForegroundColor White
} catch {
    Write-Host "[FAILED] Logstash is not accessible: $_" -ForegroundColor Red
    exit 1
}

# Test 2: Check pipeline stats
Write-Host "`n[TEST 2] Checking Logstash pipelines..." -ForegroundColor Yellow
try {
    $pipelines = Invoke-RestMethod -Uri "$LOGSTASH_HOST/_node/stats/pipelines" -Method Get -ErrorAction Stop
    Write-Host "[SUCCESS] Retrieved pipeline statistics" -ForegroundColor Green
    
    foreach ($pipeline in $pipelines.pipelines.PSObject.Properties) {
        Write-Host "  Pipeline: $($pipeline.Name)" -ForegroundColor White
        Write-Host "    Events In: $($pipeline.Value.events.in)" -ForegroundColor White
        Write-Host "    Events Out: $($pipeline.Value.events.out)" -ForegroundColor White
        Write-Host "    Events Filtered: $($pipeline.Value.events.filtered)" -ForegroundColor White
    }
} catch {
    Write-Host "[FAILED] Could not retrieve pipeline stats: $_" -ForegroundColor Red
}

# Test 3: Check plugins
Write-Host "`n[TEST 3] Checking loaded plugins..." -ForegroundColor Yellow
try {
    $plugins = Invoke-RestMethod -Uri "$LOGSTASH_HOST/_node/plugins" -Method Get -ErrorAction Stop
    Write-Host "[SUCCESS] Found $($plugins.plugins.Count) plugins loaded" -ForegroundColor Green
    Write-Host "  Inputs: $($plugins.plugins | Where-Object { $_.type -eq 'input' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor White
    Write-Host "  Filters: $($plugins.plugins | Where-Object { $_.type -eq 'filter' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor White
    Write-Host "  Outputs: $($plugins.plugins | Where-Object { $_.type -eq 'output' } | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor White
} catch {
    Write-Host "[FAILED] Could not retrieve plugins: $_" -ForegroundColor Red
}

$endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[$endTimestamp] Logstash Test Completed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
