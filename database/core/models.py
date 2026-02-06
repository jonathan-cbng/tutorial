#######################################################################################################################
"""
Database ORM models and enums for the backend.

Contains all SQLModel ORM models (table=True), enums, and mixins used for database tables.
"""

# Ignore None comparison warning for SQLAlchemy
#######################################################################################################################
# Imports
#######################################################################################################################
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel

from .helpers import HelperMixin

#######################################################################################################################
# Globals
#######################################################################################################################

NAME_LENGTH = 80
PANEL_CLASS_LENGTH = 32

#######################################################################################################################
# Body
#######################################################################################################################


# Enumerations
class Species(str, Enum):
    """Enumeration of supported animal species."""

    CANINE = "Canine"
    FELINE = "Feline"
    EQUINE = "Equine"


class Sex(str, Enum):
    """Enumeration of supported animal sexes."""

    MALE = "Male"
    MALE_NEUTERED = "Male neutered"
    FEMALE = "Female"
    FEMALE_NEUTERED = "Female neutered"
    UNKNOWN = "Unknown"


class Breed(HelperMixin, SQLModel, table=True):
    """Database model for animal breeds."""

    __tablename__ = "breed"
    id: int = Field(default=None, primary_key=True, index=True, description="Breed ID.")
    name: str = Field(index=True, nullable=False, max_length=NAME_LENGTH, description="Breed name.")
    species: Species = Field(index=True, description="Species this breed belongs to.")


class Case(HelperMixin, SQLModel, table=True):
    """Database model for animal cases."""

    __tablename__ = "case"
    id: int = Field(default=None, primary_key=True, index=True, description="Case ID.")
    name: str = Field(index=True, nullable=False, max_length=NAME_LENGTH, description="Case name.")
    owner: str | None = Field(default=None, description="Owner of the animal.")
    practice_animal_id: str | None = Field(default=None, description="Practice animal ID.")
    chip_id: str | None = Field(default=None, description="Microchip ID.")
    sex: Sex = Field(default=Sex.UNKNOWN, description="Sex of the animal.")
    birth_date: str | None = Field(default=None, description="Birth date (YYYY-MM-DD).")
    create_date: str | None = Field(default=None, description="Case creation date (YYYY-MM-DD).")
    notes: str | None = Field(default=None, description="Additional notes.")
    breed_id: int = Field(foreign_key="breed.id", description="ID of the breed.")
    breed: Breed | None = Relationship()


#######################################################################################################################
# End of file
#######################################################################################################################
