# Internal imports
from API.config.database import engine
from API.models import Base


def create_tables():
    """Creates all tables in the database."""
    Base.metadata.create_all(bind=engine)
