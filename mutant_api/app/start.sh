#!/bin/bash

# Function to check environment variables
check_env_vars() {
    local required_vars=(DB_USER DB_PASSWORD DB_HOST DB_NAME)
    local missing_vars=0
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo "Error: $var is not set"
            missing_vars=1
        else
            echo "$var is configured"
        fi
    done
    
    if [ "$missing_vars" -eq 1 ]; then
        echo "Some required environment variables are missing"
        exit 1
    fi
}

# Function to wait for the database to be available
wait_for_db() {
    echo "Waiting for database to be ready..."
    while ! mysqladmin ping -h"$DB_HOST" -P"${DB_PORT:-3306}" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
        echo "Database is not ready. Waiting..."
        sleep 2
    done
    echo "Database is ready!"
}

echo "Checking environment variables..."
check_env_vars

echo "Checking database connection..."
wait_for_db

echo "Running database migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "Migrations completed successfully"
    echo "Starting application..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000
else
    echo "Migration failed!"
    exit 1
fi