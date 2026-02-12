"""
Fix task_history action_type check constraint to include all enum values.
"""

from sqlalchemy import text
from src.db.session import engine

def fix_action_type_constraint():
    """Drop and recreate the action_type check constraint with all enum values."""
    
    with engine.begin() as conn:
        # Drop the old constraint
        print("Dropping old constraint...")
        conn.execute(text("""
            ALTER TABLE task_history 
            DROP CONSTRAINT IF EXISTS task_history_action_type_check
        """))
        
        # Add new constraint with all enum values
        print("Adding new constraint with all action types...")
        conn.execute(text("""
            ALTER TABLE task_history 
            ADD CONSTRAINT task_history_action_type_check 
            CHECK (action_type IN ('CREATED', 'UPDATED', 'COMPLETED', 'DELETED', 'ARCHIVED', 'RESTORED'))
        """))
        
        print("✅ Constraint fixed successfully!")
        
        # Verify the constraint
        result = conn.execute(text("""
            SELECT constraint_name, check_clause 
            FROM information_schema.check_constraints 
            WHERE constraint_name = 'task_history_action_type_check'
        """))
        
        for row in result:
            print(f"\nNew constraint definition:")
            print(f"Name: {row[0]}")
            print(f"Check: {row[1]}")

if __name__ == "__main__":
    try:
        fix_action_type_constraint()
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
