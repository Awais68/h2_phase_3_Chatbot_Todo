from src.db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text(
        "SELECT constraint_name, check_clause "
        "FROM information_schema.check_constraints "
        "WHERE constraint_name = 'task_history_action_type_check'"
    ))
    for row in result:
        print(f"Constraint: {row[0]}")
        print(f"Check Clause: {row[1]}")
