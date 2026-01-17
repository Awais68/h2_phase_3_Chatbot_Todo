"""
Migration script to add users table to Neon PostgreSQL database
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def add_users_table():
    """Add users table to database"""
    with engine.connect() as conn:
        # Create users table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                email VARCHAR UNIQUE NOT NULL,
                email_verified BOOLEAN DEFAULT FALSE,
                image VARCHAR,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """))
        
        # Create index on email
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        """))
        
        conn.commit()
        print("✅ Users table created successfully!")

if __name__ == "__main__":
    print("Adding users table to Neon database...")
    add_users_table()
    print("Migration complete!")
