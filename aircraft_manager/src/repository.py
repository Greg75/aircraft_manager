# Third party imports
import logging
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound, IntegrityError
from typing import List, Dict

# Internal imports
from API.schemas import AircraftBaseSchema, AircraftUpdateSchema, AircraftDisplaySchema, AircraftDataUpdateSchema
from API.models import Aircraft, AircraftData


logger = logging.getLogger(__name__)


class AircraftRepository:
    """
    Repository class to manage operations related to the Aircraft and AircraftData tables.

    Attributes:
        session (Session): The SQLAlchemy session used for database transactions.

    Methods:
        add_aircraft(aircraft: AircraftBaseSchema) -> AircraftDisplaySchema:
            Adds a new aircraft to the database.
        display_aircrafts() -> List[AircraftDisplaySchema]:
            Retrieves and returns all aircraft in the database.
        update_aircraft(aircraft_id: int, **kwargs) -> AircraftUpdateSchema:
            Updates an existing aircraft based on the provided aircraft_id and field values.
        delete_aircraft(aircraft_id: int) -> None:
            Deletes the aircraft with the given aircraft_id from the database.
    """
    def __init__(self, session: Session):
        """
        Initializes AircraftRepository class.

        Arguments:
            session: SQLAlchemy session object.
        """
        self.session = session

    def is_present(self, aircraft_id: int) -> bool:
        """
        Verifies if the aircraft object with given aircraft_id exists in the database.

        Arguments:
            session {sqlalchemy.orm.Session} -- The database session,
            aircraft_id {int} -- The aircraft object id.

        Returns:
            Raises NoResultFound exception if there is no aircraft object with given aircraft_id
            or returns True otherwise.
        """
        try:
            exists = self.session.query(Aircraft).filter_by(aircraft_id=aircraft_id).exists().scalar()
            if not exists:
                logger.error(f"Aircraft with id {aircraft_id} not found.")
                raise NoResultFound(f"Aircraft with id {aircraft_id} not found")

            logger.info(f"Aircraft with id {aircraft_id} found.")
            return True

        finally:
            self.session.close()

    def add_aircraft(self, aircraft: AircraftBaseSchema) -> AircraftDisplaySchema:
        """
        Adds new Aircraft instance to the database.

        Arguments:
            aircraft: instance of Aircraft class to be added using the AircraftBaseSchema.

        Returns:
            Instance of the Aircraft class displayed according to AircraftDisplaySchema.
        """
        try:
            with self.session.begin():
                new_aircraft = Aircraft(**aircraft.model_dump(exclude={"aircraft_data"}))
                new_aircraft_data = AircraftData(**aircraft.aircraft_data.model_dump(), aircraft=new_aircraft)
                self.session.add(new_aircraft)
                self.session.add(new_aircraft_data)

            logger.info("Aircraft added successfully.")

            return AircraftDisplaySchema.model_validate(new_aircraft)

        except IntegrityError as e:
            self.session.rollback()
            logger.error(f"Integrity error adding aircraft: {str(e)}")
            raise ValueError(f"Integrity error adding aircraft: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error adding aircraft: {str(e)}")
            raise ValueError(f"Error adding aircraft: {str(e)}")

    def display_aircrafts(self) -> List[AircraftDisplaySchema]:
        """
        Returns all the aircraft in the database as a list, contains
        the Aircraft objects, using the AircraftDisplaySchema.
        """
        all_aircrafts = self.session.query(Aircraft).options(joinedload(Aircraft.aircraft_data)).all()
        return [AircraftDisplaySchema.model_validate(aircraft) for aircraft in all_aircrafts]

    def update_aircraft(self, aircraft_id: int, **kwargs) -> AircraftUpdateSchema:
        """
        Finds the aircraft instance based on the given 'id',
        and updates the elements given as a keywords arguments.

        Arguments:
            aircraft_id: id of the Aircraft instance to be updated.
            **kwargs: keyword arguments to be updated using the AircraftUpdateSchema.

        Returns:
            Aircraft object based on the AircraftUpdateSchema.
        """
        if self.is_present(aircraft_id=aircraft_id):

            try:
                ac_values = AircraftUpdateSchema(
                    **kwargs).model_dump(exclude={"aircraft_data"}, exclude_none=True)
                ac_data_values = AircraftDataUpdateSchema(
                    **kwargs.get("aircraft_data", {})).model_dump(exclude_none=True)

                if not ac_values and not ac_data_values:
                    raise ValueError("No valid fields provided to update.")

                with self.session.begin():
                    if ac_values:
                        self.session.query(Aircraft).filter_by(
                            aircraft_id=aircraft_id).update(values={**ac_values})
                    if ac_data_values:
                        self.session.query(AircraftData).filter_by(
                            aircraft_id=aircraft_id).update(values={**ac_data_values})

                updated_aircraft = (self.session.query(Aircraft).filter_by(
                    aircraft_id=aircraft_id).options(joinedload(Aircraft.aircraft_data)).first())
                logger.info(f"Aircraft with id {aircraft_id} updated successfully.")

                return AircraftUpdateSchema.model_validate(updated_aircraft)

            except NoResultFound as e:
                logger.error(f"Aircraft with id {aircraft_id} not found: {str(e)}")
                raise ValueError(f"Error {e}")

            except IntegrityError as e:
                self.session.rollback()
                logger.error(f"Integrity error updating aircraft: {str(e)}")
                raise ValueError(f"Integrity error updating aircraft: {str(e)}")

            except Exception as e:
                logger.error(f"Unexpected error updating aircraft: {str(e)}")
                raise ValueError(f"Unexpected error: {str(e)}")

    def delete_aircraft(self, aircraft_id: int) -> Dict[str, str]:
        """
        Deletes the aircraft instance of given 'id' from the database.

        Arguments:
              aircraft_id (int): The 'id' of the Aircraft to delete.

        Returns:
                Dict[str, str]: A confirmation message.
        """
        try:
            if self.is_present(aircraft_id=aircraft_id):
                with self.session.begin():
                    self.session.query(Aircraft).filter_by(aircraft_id=aircraft_id).delete()
                    logger.info(f"Aircraft with id {aircraft_id} deleted successfully.")

                return {"message": f"Aircraft with id {aircraft_id} deleted successfully."}

        except IntegrityError as e:
            self.session.rollback()
            logger.error(f"Integrity error deleting aircraft: {str(e)}")
            raise ValueError(f"Integrity error deleting aircraft: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error deleting aircraft: {str(e)}")
            raise ValueError(f"Unexpected error: {str(e)}")