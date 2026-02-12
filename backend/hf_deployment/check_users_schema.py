from src.db.session import engine
from sqlalchemy import text, inspect

def check_users_table():
    """Check the users table schema"""
    
    with engine.connect() as conn:
        # Get table columns
        inspector = inspect(engine)
        
        if 'users' in inspector.get_table_names():
            columns = inspector.get_columns('users')
            print("Users table columns:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
        else:
            print("Users table does not exist")

if __name__ == "__main__":
    check_users_table()
