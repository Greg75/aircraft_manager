# Third party imports
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Internal imports
from aircraft_manager.src.config.database import get_db
from aircraft_manager.src.schemas import (AircraftBaseSchema, AircraftUpdateSchema, AircraftDisplaySchema,
                                          InputAircraftPerformanceRangeSchema, OutputAircraftPerformanceRangeSchema,
                                          InputAircraftPerformanceEnduranceSchema,
                                          OutputAircraftPerformanceEnduranceSchema)
from aircraft_manager.src.repository import AircraftRepository
from aircraft_manager.src.use_cases.performance import Performance

router = APIRouter(prefix="/aircrafts")


@router.get(
    path="/",
    response_model=list[AircraftDisplaySchema],
    status_code=200
)
async def show_aircrafts(session: Session = Depends(get_db)) -> list[AircraftDisplaySchema]:
    """Shows all the Aircraft objects in the database.

    Arguments:
        session {Session} -- Database session.

    Returns:
        list[AircraftDisplaySchema] -- List of Aircraft objects.
    """
    aircraft_repo = AircraftRepository(session)
    return aircraft_repo.display_aircrafts()


@router.post(
    path="/add_aircraft/",
    response_model=AircraftDisplaySchema,
    status_code=201
)
def input_aircraft(aircraft: AircraftBaseSchema,
                   session: Session = Depends(get_db)) -> AircraftDisplaySchema:
    """Adds an Aircraft object to the database.

    Arguments:
        aircraft {AircraftDataBaseSchema} -- Aircraft object,
        session {Session} -- Database session.

    Returns:
        AircraftBaseSchema -- added Aircraft object.
    """
    aircraft_repo = AircraftRepository(session)
    return aircraft_repo.add_aircraft(aircraft)


@router.patch(
    path="/update_aircraft/{aircraft_id}",
    response_model=AircraftUpdateSchema,
    status_code=200
)
def modify_aircraft(aircraft_id: int, aircraft: AircraftUpdateSchema,
                    session: Session = Depends(get_db)) -> AircraftUpdateSchema:
    """Updates an Aircraft object in the database.

    Arguments:
        aircraft_id {int} -- Aircraft ID,
        aircraft {AircraftUpdateSchema} -- Aircraft object in the shape of AircraftUpdateSchema,
        session {Session} -- Database session.

    Returns:
        AircraftUpdateSchema -- Updated Aircraft object.
    """
    aircraft_repo = AircraftRepository(session)
    return aircraft_repo.update_aircraft(aircraft_id, **aircraft.model_dump(exclude_none=True))


@router.delete(
    path="/delete_aircraft/{aircraft_id}",
    status_code=204
)
def remove_aircraft(aircraft_id: int, session: Session = Depends(get_db)):
    """Deletes an Aircraft object from the database.

    Arguments:
        aircraft_id {int} -- Aircraft ID,
        session {Session} -- Database session.

    Returns:
        dict -- confirmation message that Aircraft object was deleted.
    """
    aircraft_repo = AircraftRepository(session)
    aircraft_repo.delete_aircraft(aircraft_id)
    return {"message": "Aircraft deleted."}


@router.get(
    path="/performance/range/{}".format(
        "/".join([f"{key}" for key in InputAircraftPerformanceRangeSchema.__dict__['__pydantic_fields__'].keys()])),
    response_model=OutputAircraftPerformanceRangeSchema,
    status_code=200
)
def get_range(aircraft: InputAircraftPerformanceRangeSchema = Depends(),
              session: Session = Depends(get_db)) -> OutputAircraftPerformanceRangeSchema:
    """Gets range of the aircraft based on the data given according to InputAircraftPerformanceSchema.

    Arguments:
        aircraft {InputAircraftPerformanceRangeSchema} -- Aircraft object,
        session {Session} -- Database session.

    Returns:
        OutputAircraftPerformanceRangeSchema -- Name and range of the aircraft.
    """
    performance = Performance(session)
    return performance.calculate_range(aircraft)


@router.get(
    path="/performance/endurance/{}".format(
        "/".join([f"{key}" for key in InputAircraftPerformanceEnduranceSchema.__dict__['__pydantic_fields__'].keys()])),
    response_model=OutputAircraftPerformanceEnduranceSchema,
    status_code=200
)
def get_endurance(aircraft: InputAircraftPerformanceEnduranceSchema = Depends(),
                  session: Session = Depends(get_db)) -> OutputAircraftPerformanceEnduranceSchema:
    """Gets endurance of the aircraft based on the data given according to InputAircraftPerformanceEnduranceSchema.

    Arguments:
        aircraft {InputAircraftPerformanceEnduranceSchema} -- Aircraft object,
        session {Session} -- Database session.

    Returns:
        OutputAircraftPerformanceEnduranceSchema -- Name and endurance of the aircraft.
    """
    performance = Performance(session)
    return performance.calculate_endurance(aircraft)
