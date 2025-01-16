# Internal imports
from aircraft_manager.src.config.database import engine
from aircraft_manager.src.models import Base


def create_tables():
    """Creates all tables in the database."""
    Base.metadata.create_all(bind=engine)
