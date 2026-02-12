from src.db.session import engine
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text('DROP TABLE IF EXISTS backend_users CASCADE'))
    print("✅ backend_users table dropped")
