# Third party imports
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
connection = engine.connect()


SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    """Create a database session.
    Yields:
        Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
