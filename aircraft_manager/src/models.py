# Third party imports
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from enum import Enum, unique


@unique
class AircraftType(int, Enum):
    Fighter: int = 1
    Striker: int = 2
    Bomber: int = 3
    Trainer: int = 4


class Base(DeclarativeBase):
    """Basic model to inherit from."""
    pass


class Aircraft(Base):
    """Model of the 'parent' aircraft table, dedicated to store basic information about the aircraft."""

    __tablename__ = 'aircrafts'

    aircraft_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    manufacturer: Mapped[str] = mapped_column(nullable=False)
    aircraft_type: Mapped["AircraftType"] = mapped_column(nullable=False)
    first_flight: Mapped[str] = mapped_column(nullable=True)
    aircraft_data: Mapped["AircraftData"] = relationship(argument="AircraftData",
                                                         back_populates="aircraft",
                                                         cascade="all, delete")


class AircraftData(Base):
    """Model of the 'child' aircraft_data table, dedicated to store additional information about the aircraft."""

    __tablename__ = 'aircrafts_data'

    aircraft_data_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    fuel_consumption: Mapped[int] = mapped_column(nullable=True)
    ceiling: Mapped[int] = mapped_column(nullable=True)
    weight: Mapped[int] = mapped_column(nullable=True)
    fuel: Mapped[int] = mapped_column(nullable=True)
    take_off_weight: Mapped[int] = mapped_column(nullable=True)
    max_speed: Mapped[int] = mapped_column(nullable=True)
    cruise_speed: Mapped[int] = mapped_column(nullable=True)
    aircraft_id: Mapped[int] = mapped_column(ForeignKey(column="aircrafts.aircraft_id",
                                                        ondelete="CASCADE"), unique=True)
    aircraft: Mapped["Aircraft"] = relationship(argument="Aircraft",
                                                back_populates="aircraft_data",
                                                single_parent=True)
