# Component Tests

This folder contains test scripts for each component of the Big Data project. Each script tests the component's functionality and logs results to the terminal.

## Available Test Scripts

### Individual Component Tests

- **test-elasticsearch.ps1** - Tests Elasticsearch connectivity, health, indices, and search functionality
- **test-redis.ps1** - Tests Redis connectivity and basic operations
- **test-logstash.ps1** - Tests Logstash API, pipeline status, and plugins
- **test-kibana.ps1** - Tests Kibana status and connectivity to Elasticsearch
- **test-django.ps1** - Tests Django API endpoints, database connectivity, and file upload
- **test-angular.ps1** - Tests Angular application accessibility and static resources

### Complete System Test

- **test-all.ps1** - Runs all component tests and provides a summary

## Usage

### Run Individual Tests

```powershell
# Test Elasticsearch
.\test-elasticsearch.ps1

# Test Redis
.\test-redis.ps1

# Test Logstash
.\test-logstash.ps1

# Test Kibana
.\test-kibana.ps1

# Test Django API
.\test-django.ps1

# Test Angular App
.\test-angular.ps1
```

### Run All Tests

```powershell
# Run all tests sequentially
.\test-all.ps1

# Run all tests in parallel
.\test-all.ps1 -Parallel
```

## Prerequisites

- PowerShell 5.1 or higher
- All components should be running (via docker-compose or manually)
- Network access to component ports:
  - Elasticsearch: 9200
  - Redis: 6379
  - Logstash: 9600
  - Kibana: 5601
  - Django: 8000
  - Angular: 4200

## Output

Each test script provides:
- ✅ **SUCCESS** messages in green for passed tests
- ❌ **FAILED** messages in red for failed tests
- ⚠️ **WARNING** messages in yellow for partial failures
- ℹ️ **INFO** messages for additional information
- Timestamps for each test run
- Detailed component information (versions, stats, etc.)

## Example Output

```
========================================
[2026-01-05 14:30:00] Starting Elasticsearch Test
========================================

[TEST 1] Checking Elasticsearch health...
[SUCCESS] Elasticsearch is running
  Status: green
  Cluster Name: docker-cluster
  Number of Nodes: 1

[TEST 2] Listing Elasticsearch indices...
[SUCCESS] Found 5 indices
  - logs_capteurs (docs: 1000)
  - logs_alertes (docs: 500)
  ...

========================================
[2026-01-05 14:30:15] Elasticsearch Test Completed
========================================
```

## Troubleshooting

If tests fail:

1. **Check if Docker containers are running:**
   ```powershell
   docker ps
   ```

2. **Check component logs:**
   ```powershell
   docker-compose logs [service-name]
   ```

3. **Verify port accessibility:**
   ```powershell
   Test-NetConnection -ComputerName localhost -Port [port-number]
   ```

4. **Restart services:**
   ```powershell
   docker-compose restart [service-name]
   ```

## Adding New Tests

To add a new component test:

1. Create a new PowerShell script: `test-[component].ps1`
2. Follow the existing script structure:
   - Add header and timestamp
   - Implement test cases
   - Use color-coded output
   - Add completion timestamp
3. Update `test-all.ps1` to include the new test
4. Update this README

## Notes

- Tests are non-destructive and don't modify data
- Some tests may show warnings for optional features
- Run tests after starting all services with docker-compose
- Tests can be scheduled using Windows Task Scheduler
