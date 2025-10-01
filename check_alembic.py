import sqlalchemy
from sqlalchemy import text

def check_alembic_version():
    try:
        engine = sqlalchemy.create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/driveusta')
        with engine.connect() as conn:
            result = conn.execute(text('SELECT * FROM alembic_version'))
            row = result.fetchone()
            if row:
                print(f"Current alembic version: {row[0]}")
            else:
                print("No alembic version found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_alembic_version()