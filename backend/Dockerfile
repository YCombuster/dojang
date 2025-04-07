FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    libyaml-dev \
    && rm -rf /var/lib/apt/lists/

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Install PyYAML with Cython first to avoid build issues
RUN pip install Cython
RUN pip install PyYAML==6.0.1

# Copy requirements file first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the app as a module for proper imports in tests
RUN pip install --no-cache-dir -e .
RUN pip freeze > /app/installed_packages.txt

# Expose the port the app runs on
EXPOSE 8000

# Create a script to run tests with proper environment variables
RUN echo '#!/bin/bash\n\
export PYTHONPATH=$PYTHONPATH:/app\n\
if [ "$#" -eq 0 ]; then\n\
  echo "Running all tests..."\n\
  pytest -v\n\
elif [ "$1" = "db" ]; then\n\
  echo "Testing database connection and pgvector..."\n\
  pytest -v tests/test_database.py\n\
elif [ "$1" = "api" ]; then\n\
  echo "Testing API endpoints..."\n\
  pytest -v tests/test_api.py\n\
else\n\
  pytest "$@"\n\
fi\n\
' > /usr/local/bin/run-tests && \
chmod +x /usr/local/bin/run-tests

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 