# Run tests in Docker container
if ($args[0] -eq "db") {
    Write-Host "Testing database connection and pgvector..." -ForegroundColor Green
    docker compose exec backend /usr/local/bin/run-tests db
}
elseif ($args[0] -eq "api") {
    Write-Host "Testing API endpoints..." -ForegroundColor Green
    docker compose exec backend /usr/local/bin/run-tests api
}
else {
    Write-Host "Running all tests..." -ForegroundColor Green
    docker compose exec backend /usr/local/bin/run-tests $args
} 