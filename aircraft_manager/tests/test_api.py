# Third party imports
import asyncio
from fastapi.testclient import TestClient

# Internal imports
from aircraft_manager.src.models import Aircraft
from aircraft_manager.tests.conftest import db_session, load_data, new_aircraft_fixture
from aircraft_manager.src.repository import AircraftRepository


def test_health_check(client: TestClient):
    """Tests the 'health' endpoint of the application. This test verifies that the client is working as expected.

    Arguments:
        client {TestClient} -- fastapi.testclient object.

    Expected behaviour:
        health_check() -> {'status': 'OK'}.
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "HEALTHY", "database": "OK"}


def test_show_aircrafts(client: TestClient, load_data, db_session):
    """Tests the 'show_aircrafts' endpoint of the application. This test verifies if the client is returning list of
    AircraftDisplaySchema objects correctly.

    Arguments:
         client {TestClient} -- fastapi.testclient object,
         load_data {pytest.fixture} -- creates database structure and loads data,
         db_session {sqlalchemy.orm.session} -- database session.

    Expected behaviour:
        show_aircrafts() -> list[AircraftDisplaySchema(aircraft_id=100, name='C-152', manufacturer='Cessna'...)].
    """
    response = client.get("/aircrafts/")
    data = response.json()

    assert response.status_code == 200
    assert data[0]["name"] == "C-152"


def test_input_aircraft(client: TestClient, db_session, new_aircraft_fixture):
    """Tests the 'input_aircraft' endpoint of the application. This test verifies if the client is adding new aircraft
    object into the database.

    Arguments:
        client {TestClient} -- fastapi.testclient object,
        db_session {sqlalchemy.orm.session} -- database session,
        new_aircraft {AircraftBaseSchema} -- AircraftBaseSchema object.

    Expected behaviour:
        input_aircraft() -> adds AircraftDisplaySchema(aircraft_id=100, name='C-152', manufacturer='Cessna'...)
        object into the database.
    """
    response = client.post(
        url="/aircrafts/add_aircraft",
        json=new_aircraft_fixture.model_dump()
    )

    assert response.status_code == 201

    data = response.json()
    assert data["aircraft_id"] == 101
    assert data["name"] == "C-172"
    assert data["aircraft_data"]["fuel_consumption"] == 18


def test_modify_aircraft(client: TestClient, db_session, update_aircraft, aircraft_id=100):
    """Tests the 'modify_aircraft' endpoint of the application. This test verifies if the client is modifying aircraft
    object as expected.

    Arguments:
        client {TestClient} -- fastapi.testclient object,
        db_session {sqlalchemy.orm.session} -- database session,
        update_aircraft {AircraftBaseSchema} -- pytest fixture with updated aircraft object,
        aircraft_id {int} -- aircraft id.

    Expected behaviour:
        modify_aircraft() -> AircraftUpdateSchema(aircraft_id=100, name='C-182', aircraft_data{cruise_speed=170}).
    """
    response = client.patch(
        url=f"/aircrafts/update_aircraft/{aircraft_id}",
        json=update_aircraft.model_dump(exclude_none=True)
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "C-182"
    assert data["aircraft_data"]["cruise_speed"] == 170


def test_modify_aircraft_2(client: TestClient, load_data, db_session):
    """Tests the 'modify_aircraft' endpoint of the application. This test verifies if the client is modifying aircraft
    object as expected but instead of injected 'update_aircraft' fixture, this test is retrieving aircraft data from
    the mock database and then modifies aircraft object.

    Arguments:
        client {TestClient} -- fastapi.testclient object,
        load_data {pytest.fixture} -- creates database structure and loads data,
        db_session {sqlalchemy.orm.session} -- database session.

    Expected behaviour:
        modify_aircraft() -> AircraftUpdateSchema(aircraft_id=100, name='C-100', aircraft_data{cruise_speed=190}).
    """
    aircraft_repo = AircraftRepository(db_session)
    list_of_aircrafts = aircraft_repo.display_aircrafts()
    aircraft_to_update = list_of_aircrafts[0].model_dump()

    aircraft_id = aircraft_to_update["aircraft_id"]

    aircraft_to_update["name"] = "C-100"
    aircraft_to_update["aircraft_data"]["cruise_speed"] = 190

    response = client.patch(
        url=f"/aircrafts/update_aircraft/{aircraft_id}",
        json=aircraft_to_update
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "C-100"
    assert data["aircraft_data"]["cruise_speed"] == 190


def test_remove_aircraft(client: TestClient, db_session, aircraft_id=100):
    """Tests 'remove_aircraft' endpoint of the application. This test verifies if the client is removing pointed
    aircraft object from the database.

    Arguments:
        client {TestClient} -- fastapi.testclient object,
        db_session {sqlalchemy.orm.session} -- database session,
        aircraft_id {int} -- aircraft id.

    Expected behaviour:
        remove_aircraft() -> Aircraft object is None.
    """
    response = client.delete(
        url=f"/aircrafts/delete_aircraft/{aircraft_id}"
    )

    assert response.status_code == 204

    data = db_session.query(Aircraft).filter_by(aircraft_id=100).first()
    assert data is None
