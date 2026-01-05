# Test Elasticsearch Component
# This script tests Elasticsearch connectivity and basic operations

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$ES_HOST = "http://localhost:9200"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[$timestamp] Starting Elasticsearch Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Test 1: Check Elasticsearch health
Write-Host "`n[TEST 1] Checking Elasticsearch health..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$ES_HOST/_cluster/health" -Method Get -ErrorAction Stop
    Write-Host "[SUCCESS] Elasticsearch is running" -ForegroundColor Green
    Write-Host "  Status: $($response.status)" -ForegroundColor White
    Write-Host "  Cluster Name: $($response.cluster_name)" -ForegroundColor White
    Write-Host "  Number of Nodes: $($response.number_of_nodes)" -ForegroundColor White
} catch {
    Write-Host "[FAILED] Elasticsearch is not accessible: $_" -ForegroundColor Red
    exit 1
}

# Test 2: List all indices
Write-Host "`n[TEST 2] Listing Elasticsearch indices..." -ForegroundColor Yellow
try {
    $indices = Invoke-RestMethod -Uri "$ES_HOST/_cat/indices?format=json" -Method Get -ErrorAction Stop
    Write-Host "[SUCCESS] Found $($indices.Count) indices" -ForegroundColor Green
    foreach ($index in $indices) {
        Write-Host "  - $($index.index) (docs: $($index.'docs.count'))" -ForegroundColor White
    }
} catch {
    Write-Host "[FAILED] Could not list indices: $_" -ForegroundColor Red
}

# Test 3: Test search functionality
Write-Host "`n[TEST 3] Testing search functionality..." -ForegroundColor Yellow
try {
    $searchBody = @{
        query = @{
            match_all = @{}
        }
        size = 1
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$ES_HOST/_search" -Method Post -Body $searchBody -ContentType "application/json" -ErrorAction Stop
    Write-Host "[SUCCESS] Search is working" -ForegroundColor Green
    Write-Host "  Total documents: $($response.hits.total.value)" -ForegroundColor White
} catch {
    Write-Host "[FAILED] Search test failed: $_" -ForegroundColor Red
}

$endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[$endTimestamp] Elasticsearch Test Completed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
