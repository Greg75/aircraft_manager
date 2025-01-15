# Third party imports
import pytest
from typing import Generator, Callable
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session

# Internal imports
from aircraft_manager.src.models import Base, Aircraft, AircraftData, AircraftType
from aircraft_manager.src.schemas import AircraftBaseSchema, AircraftUpdateSchema, AircraftDisplaySchema

DATABASE_URL = "sqlite://"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
Local_session = sessionmaker(bind=engine)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """
    Yields database session based on the engine bound by 'sessionmaker' class.
    """

    local_session = Local_session()
    try:
        yield local_session
    finally:
        local_session.rollback()
        local_session.close()


@pytest.fixture
def load_data(db_session: Session) -> None:
    """
    Creates tables in database and loads data into the database.

    Arguments:
        db_session {sqlalchemy.orm.session} -- Database session object.
    """
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    except Exception as exp:
        pytest.fail(f"Database setup failed: {exp}.")

    aircraft_data = AircraftData(
        aircraft_data_id=100,
        fuel_consumption=15,
        ceiling=2800,
        weight=750,
        fuel=120,
        take_off_weight=870,
        max_speed=270,
        cruise_speed=190
    )

    aircraft = Aircraft(
        aircraft_id=100,
        name="C-152",
        manufacturer="Cessna",
        aircraft_type=AircraftType.Trainer,
        first_flight="1972-08-12",
        aircraft_data=aircraft_data
    )

    db_session.add(aircraft)
    db_session.flush()


@pytest.fixture
def override_get_db(db_session: Session) -> Callable:
    """
    Returns generator function that yields database session object.

    Arguments:
        db_session {sqlalchemy.orm.session} -- Database session object.
    """
    def generate_db():
        """
        Yields the test database session for dependency injection.
        """
        yield db_session

    return generate_db


@pytest.fixture
def app(override_get_db: Callable) -> FastAPI:
    """
    Returns FastAPI application.

    Arguments:
        override_get_db {Callable} -- Function that returns database session object.
    """
    from aircraft_manager.src.main import app
    from aircraft_manager.src.config.database import get_db

    app.dependency_overrides[get_db] = override_get_db

    return app


@pytest.fixture
def client(app: FastAPI, load_data) -> Generator[TestClient, None, None]:
    """
    Yields FastAPI client.

    Arguments:
        app {FastAPI} -- FastAPI application,
        load_data {Callable} -- Function that creates database and loads data into database.
    """
    with TestClient(app=app, base_url="http://test") as tc:
        yield tc


def to_schema(aircraft: Aircraft) -> dict:
    """
    Convert aircraft object into dictionary compatible with schema.

    Arguments:
        aircraft {Aircraft} -- Aircraft object to convert.

    Returns:
        dict -- Dictionary representation of the Aircraft object with nested AircraftData.
    """
    return {
        **aircraft.__dict__,
        "aircraft_data": aircraft.aircraft_data.__dict__
    }


@pytest.fixture
def new_aircraft_fixture(create_aircraft) -> AircraftDisplaySchema:
    """
    Returns AircraftBaseSchema instance with sample data for testing.

    Arguments:
        create_aircraft {Aircraft} -- Callable that creates mocked Aircraft object.

    Returns:
        AircraftBaseSchema -- Schema instance populated with sample aircraft data.
    """
    aircraft = Aircraft(
        aircraft_id=101,
        name="C-172",
        manufacturer="Cessna",
        aircraft_type=AircraftType.Trainer,
        first_flight="1972-08-16",
        aircraft_data=AircraftData(
            aircraft_data_id=101,
            fuel_consumption=18,
            ceiling=3200,
            weight=870,
            fuel=150,
            take_off_weight=1020,
            max_speed=270,
            cruise_speed=210
        )
    )
    print(AircraftDisplaySchema(**to_schema(aircraft)))
    return AircraftDisplaySchema(**to_schema(aircraft))


@pytest.fixture
def update_aircraft() -> AircraftUpdateSchema:
    """
    Return AircraftUpdateSchema instance.
    """

    aircraft_data = AircraftData(
        aircraft_data_id=100,
        fuel_consumption=15,
        ceiling=2800,
        weight=750,
        fuel=120,
        take_off_weight=870,
        max_speed=270,
        cruise_speed=170
    )

    aircraft = Aircraft(
        aircraft_id=100,
        name="C-182",
        manufacturer="Cessna",
        aircraft_type=AircraftType.Trainer,
        first_flight="1972-08-12",
        aircraft_data=aircraft_data
    )

    return AircraftUpdateSchema(**to_schema(aircraft))


@pytest.fixture
def create_aircraft(**kwargs) -> Aircraft:
    return Aircraft(
        aircraft_id=kwargs.get("aircraft_id"),
        name=kwargs.get("name"),
        manufacturer=kwargs.get("manufacturer"),
        aircraft_type=kwargs.get("aircraft_type"),
        first_flight=kwargs.get("first_flight"),
        aircraft_data=AircraftData(
            aircraft_data_id=kwargs.get("aircraft_data_id"),
            fuel_consumption=kwargs.get("fuel_consumption"),
            ceiling=kwargs.get("ceiling"),
            weight=kwargs.get("weight"),
            fuel=kwargs.get("fuel"),
            take_off_weight=kwargs.get("take_off_weight"),
            max_speed=kwargs.get("max_speed"),
            cruise_speed=kwargs.get("cruise_speed")
        )
    )
