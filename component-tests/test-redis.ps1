# Test Redis Component
# This script tests Redis connectivity and basic operations

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$REDIS_HOST = "localhost"
$REDIS_PORT = 6379

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[$timestamp] Starting Redis Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Test 1: Check if Redis is running
Write-Host "`n[TEST 1] Checking Redis connectivity..." -ForegroundColor Yellow
try {
    $tcpConnection = Test-NetConnection -ComputerName $REDIS_HOST -Port $REDIS_PORT -WarningAction SilentlyContinue
    if ($tcpConnection.TcpTestSucceeded) {
        Write-Host "[SUCCESS] Redis is accessible on port $REDIS_PORT" -ForegroundColor Green
    } else {
        Write-Host "[FAILED] Redis is not accessible on port $REDIS_PORT" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[FAILED] Could not connect to Redis: $_" -ForegroundColor Red
    exit 1
}

# Test 2: Check Redis using redis-cli (if available)
Write-Host "`n[TEST 2] Testing Redis operations..." -ForegroundColor Yellow
try {
    $redisCli = Get-Command redis-cli -ErrorAction SilentlyContinue
    if ($redisCli) {
        $pingResult = redis-cli -h $REDIS_HOST -p $REDIS_PORT PING
        if ($pingResult -eq "PONG") {
            Write-Host "[SUCCESS] Redis PING successful" -ForegroundColor Green
        }
        
        # Test SET and GET
        redis-cli -h $REDIS_HOST -p $REDIS_PORT SET test_key "test_value" | Out-Null
        $getValue = redis-cli -h $REDIS_HOST -p $REDIS_PORT GET test_key
        if ($getValue -eq "test_value") {
            Write-Host "[SUCCESS] Redis SET/GET operations working" -ForegroundColor Green
        }
        redis-cli -h $REDIS_HOST -p $REDIS_PORT DEL test_key | Out-Null
        
        # Check queue length
        $queueLength = redis-cli -h $REDIS_HOST -p $REDIS_PORT LLEN logstash
        Write-Host "  Logstash queue length: $queueLength" -ForegroundColor White
    } else {
        Write-Host "[WARNING] redis-cli not found, skipping detailed tests" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARNING] Redis operations test partially failed: $_" -ForegroundColor Yellow
}

$endTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "[$endTimestamp] Redis Test Completed" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
