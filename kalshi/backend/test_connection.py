from sqlalchemy import text

from app.database import engine

print("Connecting to PostgreSQL database...")

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print(result.scalar())

except Exception as e:
    print(f"❌ Connection failed. Error Message: {e}")