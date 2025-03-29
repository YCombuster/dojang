#!/bin/bash
# Run tests in Docker container

if [ "$1" = "db" ]; then
  echo -e "\033[0;32mTesting database connection and pgvector...\033[0m"
  docker compose exec backend /usr/local/bin/run-tests db
elif [ "$1" = "api" ]; then
  echo -e "\033[0;32mTesting API endpoints...\033[0m"
  docker compose exec backend /usr/local/bin/run-tests api
else
  echo -e "\033[0;32mRunning all tests...\033[0m"
  docker compose exec backend /usr/local/bin/run-tests "$@"
fi 