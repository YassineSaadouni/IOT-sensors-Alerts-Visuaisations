# Test All Components
# This script runs all component tests and provides a summary

param(
    [switch]$Parallel = $false
)

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "========================================" -ForegroundColor Magenta
Write-Host "[$timestamp] Starting Complete System Test" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta

# Define all test scripts
$testScripts = @(
    @{Name="Elasticsearch"; Script="test-elasticsearch.ps1"},
    @{Name="Redis"; Script="test-redis.ps1"},
    @{Name="Logstash"; Script="test-logstash.ps1"},
    @{Name="Kibana"; Script="test-kibana.ps1"},
    @{Name="Django API"; Script="test-django.ps1"},
    @{Name="Angular App"; Script="test-angular.ps1"}
)

$results = @{}

if ($Parallel) {
    Write-Host "`nRunning tests in parallel mode..." -ForegroundColor Yellow
    
    $jobs = @()
    foreach ($test in $testScripts) {
        $scriptPath = Join-Path $scriptDir $test.Script
        $jobs += Start-Job -ScriptBlock {
            param($path)
            & $path
        } -ArgumentList $scriptPath -Name $test.Name
    }
    
    # Wait for all jobs and collect results
    foreach ($job in $jobs) {
        Write-Host "`nWaiting for $($job.Name) test..." -ForegroundColor Cyan
        $output = Receive-Job -Job $job -Wait
        Write-Host $output
        $results[$job.Name] = if ($job.State -eq "Completed") { "PASSED" } else { "FAILED" }
        Remove-Job -Job $job
    }
} else {
    Write-Host "`nRunning tests sequentially..." -ForegroundColor Yellow
    
    foreach ($test in $testScripts) {
        Write-Host "`n`n" -NoNewline
        $scriptPath = Join-Path $scriptDir $test.Script
        
        if (Test-Path $scriptPath) {
            try {
                & $scriptPath
                $results[$test.Name] = "PASSED"
            } catch {
                Write-Host "[ERROR] Test $($test.Name) encountered an error: $_" -ForegroundColor Red
                $results[$test.Name] = "FAILED"
            }
        } else {
            Write-Host "[WARNING] Test script not found: $scriptPath" -ForegroundColor Yellow
            $results[$test.Name] = "SKIPPED"
        }
        
        Start-Sleep -Seconds 2
    }
}

# Print summary
$endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "`n`n========================================" -ForegroundColor Magenta
Write-Host "[$endTimestamp] TEST SUMMARY" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta

$passed = 0
$failed = 0
$skipped = 0

foreach ($result in $results.GetEnumerator()) {
    $color = switch ($result.Value) {
        "PASSED" { "Green"; $passed++; break }
        "FAILED" { "Red"; $failed++; break }
        "SKIPPED" { "Yellow"; $skipped++; break }
        default { "White" }
    }
    
    $statusText = $result.Value.PadRight(10)
    Write-Host "$statusText : $($result.Name)" -ForegroundColor $color
}

Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "Total: $($results.Count) | Passed: $passed | Failed: $failed | Skipped: $skipped" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Magenta

if ($failed -gt 0) {
    exit 1
}
