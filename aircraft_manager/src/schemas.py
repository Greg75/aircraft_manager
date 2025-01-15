# Third party imports
from typing import Optional
from pydantic import BaseModel, ConfigDict, computed_field

# Internal imports
from aircraft_manager.src.models import AircraftType


# Aircraft Data class schemas
class AircraftDataBaseSchema(BaseModel):
    """Base AircraftData class schema with all obligatory fields."""
    model_config = ConfigDict(from_attributes=True)

    fuel_consumption: float
    ceiling: float
    weight: float
    fuel: float
    max_speed: float
    cruise_speed: float

    @computed_field
    @property
    def take_off_weight(self) -> float | None:
        """Returns take off weight if both parameters (weight and armament) are given."""
        fuel_mass_ratio = 0.7
        if self.fuel:
            fuel_weight = self.fuel * fuel_mass_ratio
        else:
            fuel_weight = 0
        return self.weight + fuel_weight if all([self.fuel, self.weight]) else self.weight


class AircraftDataUpdateSchema(AircraftDataBaseSchema):
    """Update aircraft data schema with all optional fields IOT support POST and PATCH HTTP methods."""
    fuel_consumption: Optional[float] = None
    ceiling: Optional[float] = None
    weight: Optional[float] = None
    fuel: Optional[float] = None
    max_speed: Optional[float] = None
    cruise_speed: Optional[float] = None


# Aircraft class schemas
class AircraftBaseSchema(BaseModel):
    """Base aircraft schema with all obligatory fields."""
    model_config = ConfigDict(from_attributes=True)

    name: str
    manufacturer: str
    aircraft_type: AircraftType
    first_flight: str
    aircraft_data: AircraftDataBaseSchema


class AircraftUpdateSchema(AircraftBaseSchema):
    """Update aircraft schema with all optional fields IOT support POST and PATCH HTTP methods."""
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    aircraft_type: Optional[AircraftType] = None
    first_flight: Optional[str] = None
    aircraft_data: Optional[AircraftDataUpdateSchema] = None


class AircraftDisplaySchema(AircraftBaseSchema):
    """Adds 'aircraft_id' field to the 'AircraftBaseSchema' IOT display complete aircraft data from database."""
    aircraft_id: int


class InputAircraftPerformanceRangeSchema(BaseModel):
    """Input Performance Range schema provides necessary data for maximum range calculation
    with cruise speed."""
    model_config = ConfigDict(from_attributes=True)

    aircraft_id: int
    wind_speed: float
    fuel: float


class OutputAircraftPerformanceRangeSchema(BaseModel):
    """Output Performance Range schema presents aircraft name and its maximum range."""
    model_config = ConfigDict(from_attributes=True)

    name: str
    range: float


class InputAircraftPerformanceEnduranceSchema(BaseModel):
    """Input Performance Endurance schema provides aircraft_id and fuel amount to calculate maximum aircraft
    endurance."""
    model_config = ConfigDict(from_attributes=True)

    aircraft_id: int
    fuel: float


class OutputAircraftPerformanceEnduranceSchema(BaseModel):
    """Output Performance Endurance schema provides aircraft_id and fuel amount to calculate maximum aircraft
    endurance."""
    model_config = ConfigDict(from_attributes=True)

    name: str
    endurance: str
