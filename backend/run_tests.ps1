# Run tests in Docker container
Write-Host "Running tests in Docker container..." -ForegroundColor Green
docker compose exec backend /usr/local/bin/run-tests $args 