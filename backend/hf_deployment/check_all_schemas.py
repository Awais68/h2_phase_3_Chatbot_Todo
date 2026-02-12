from sqlalchemy import inspect
from src.db.session import engine

def check_table_schemas():
    """Check relevant table schemas"""
    
    inspector = inspect(engine)
    tables_to_check = ['tasks', 'users', 'backend_users']
    
    for table_name in tables_to_check:
        if table_name in inspector.get_table_names():
            print(f"\n{table_name} table columns:")
            columns = inspector.get_columns(table_name)
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
        else:
            print(f"\n{table_name} table does not exist")

if __name__ == "__main__":
    check_table_schemas()
