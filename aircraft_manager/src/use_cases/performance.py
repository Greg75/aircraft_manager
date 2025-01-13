# Third party imports
from sqlalchemy.orm import Session
from time import gmtime, strftime

# Internal imports
from aircraft_manager.src.models import Aircraft, AircraftData
from aircraft_manager.src.schemas import (InputAircraftPerformanceRangeSchema, OutputAircraftPerformanceRangeSchema,
                         InputAircraftPerformanceEnduranceSchema, OutputAircraftPerformanceEnduranceSchema)


class Performance:
    """Performance class to manage all methods related to aircraft technical data.

    Attributes:
        session: SQLAlchemy session object.

    Methods:
        calculate_endurance(aircraft_id: int): calculates aircraft endurance
        based on weight and speed.
    """
    def __init__(self, session: Session) -> None:
        """Initializes Performance class.

        Arguments:
            session: SQLAlchemy session object.
        """
        self.session = session

    def calculate_range(self, input_data: InputAircraftPerformanceRangeSchema) -> (
            OutputAircraftPerformanceRangeSchema):
        """Calculates maximum range [km] based on the given fuel and wind speed in reference to cruise_speed saved in
        the database.

        Arguments:
            input_data: Input data provided in accordance with InputAircraftPerformanceRangeSchema.

        Returns:
            Data formatted according to the OutputAircraftPerformanceSchema.
        """
        aircraft = self.session.query(Aircraft).filter_by(aircraft_id=input_data.aircraft_id).first()
        aircraft_data = self.session.query(AircraftData).filter_by(aircraft_id=input_data.aircraft_id).first()

        calculated_range = ((aircraft_data.cruise_speed + input_data.wind_speed) * input_data.fuel /
                            aircraft_data.fuel_consumption)

        return OutputAircraftPerformanceRangeSchema(name=str(aircraft.name), range=calculated_range)

    def calculate_endurance(self, input_data: InputAircraftPerformanceEnduranceSchema) -> (
            OutputAircraftPerformanceEnduranceSchema):
        """Calculates maximum aircraft endurance [h] based on the given fuel in reference to fuel_consumption saved in
        the database.

        Arguments:
            input_data: Input data provided in accordance with InputAircraftPerformanceEnduranceSchema.

        Returns:
            Data formatted according to the OutputAircraftPerformanceEnduranceSchema.
        """
        hours_to_seconds = 3600

        aircraft = self.session.query(Aircraft).filter_by(aircraft_id=input_data.aircraft_id).first()
        aircraft_data = self.session.query(AircraftData).filter_by(aircraft_id=input_data.aircraft_id).first()

        calculated_endurance_in_seconds = input_data.fuel / (aircraft_data.fuel_consumption / hours_to_seconds)

        endurance_hours_minutes = strftime("%H:%M", gmtime(calculated_endurance_in_seconds))

        return OutputAircraftPerformanceEnduranceSchema(name=str(aircraft.name), endurance=endurance_hours_minutes)
