#!/bin/bash
# Run tests in Docker container
echo -e "\033[0;32mRunning tests in Docker container...\033[0m"
docker compose exec backend /usr/local/bin/run-tests "$@" 