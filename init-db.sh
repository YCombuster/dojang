#!/bin/bash
set -e

# Run the PostgreSQL initialization steps
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    ALTER USER postgres WITH PASSWORD 'zany12';
    CREATE EXTENSION IF NOT EXISTS vector;

    -- Knowledge Base Sources Table
    CREATE TABLE knowledge_base_sources (
        source_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        source_type VARCHAR(50),
        author VARCHAR(255),
        publisher VARCHAR(255),
        publication_date DATE,
        license VARCHAR(100),
        language VARCHAR(50),
        url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Knowledge Base Content Table
    CREATE TABLE knowledge_base_content (
        content_id SERIAL PRIMARY KEY,
        source_id INT REFERENCES knowledge_base_sources(source_id) ON DELETE CASCADE,
        parent_content_id INT REFERENCES knowledge_base_content(content_id) ON DELETE CASCADE,
        title VARCHAR(255),
        content TEXT,
        content_type VARCHAR(50),
        embedding VECTOR(768),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Users Table
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Tags Table
    CREATE TABLE tags (
        tag_id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    );

    -- Content Tags Junction Table
    CREATE TABLE content_tags (
        content_id INT REFERENCES knowledge_base_content(content_id) ON DELETE CASCADE,
        tag_id INT REFERENCES tags(tag_id) ON DELETE CASCADE,
        PRIMARY KEY (content_id, tag_id)
    );

    -- User Activity Log Table
    CREATE TABLE user_activity_log (
        activity_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id) ON DELETE SET NULL,
        content_id INT REFERENCES knowledge_base_content(content_id) ON DELETE SET NULL,
        activity_type VARCHAR(50),
        activity_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
EOSQL

# Add authentication configurations
echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf
echo "local all all trust" >> /var/lib/postgresql/data/pg_hba.conf 