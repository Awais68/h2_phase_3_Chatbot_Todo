# PostgreSQL Database Configuration for Kubernetes Deployment

# This file contains the database initialization SQL scripts for the Todo Chatbot application
# It creates the necessary database schema and initial data

# Create the database (this is typically handled by PostgreSQL when the database is created)
-- CREATE DATABASE tododb;

-- The application uses SQLModel which will create tables automatically on startup
-- However, we can provide some initial setup if needed

-- Example: Create extension if needed (PostgreSQL specific)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The actual table creation is handled by SQLModel's metadata.create_all() in the startup event
-- See backend/main.py:46 for the automatic table creation on startup