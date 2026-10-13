import sys

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "postgresql+psycopg2://dss150p:dss150p_lab@localhost:5433/dss150p_lab"


def main():
    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version();")).scalar()
            database = conn.execute(text("SELECT current_database();")).scalar()
    except SQLAlchemyError as error:
        print("Connection failed:", error)
        sys.exit(1)
    print("PostgreSQL version:", version)
    print("Current database:", database)


if __name__ == "__main__":
    main()