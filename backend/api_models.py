#######################################################################################################################
"""
API (Pydantic) models for the backend.

Contains all SQLModel/Pydantic models NOT using table=True, for API schemas and validation.
"""

from sqlmodel import Field, SQLModel

from backend.db_models import Breed, Sex


# Case API models
class CaseBase(SQLModel):
    """Base fields for case API models."""

    name: str = Field(..., description="Case name.")
    owner: str | None = Field(default=None, description="Owner of the animal.")
    practice_animal_id: str | None = Field(default=None, description="Practice animal ID.")
    chip_id: str | None = Field(default=None, description="Microchip ID.")
    sex: Sex = Field(default=Sex.UNKNOWN, description="Sex of the animal.")
    birth_date: str | None = Field(default=None, description="Birth date (YYYY-MM-DD).")
    create_date: str | None = Field(default=None, description="Case creation date (YYYY-MM-DD).")
    notes: str | None = Field(default=None, description="Additional notes.")
    breed_id: int = Field(..., description="ID of the breed.")


class CaseCreate(CaseBase):
    """Fields for creating a case via the API."""

    pass


class CaseRead(CaseBase):
    """Fields for reading a case from the API."""

    id: int = Field(..., description="Case ID.")
    breed: Breed | None = Field(default=None, description="Breed object.")


class CaseUpdate(SQLModel):
    """Fields for updating a case via the API."""

    name: str | None = Field(default=None, description="Case name.")
    owner: str | None = Field(default=None, description="Owner of the animal.")
    practice_animal_id: str | None = Field(default=None, description="Practice animal ID.")
    chip_id: str | None = Field(default=None, description="Microchip ID.")
    sex: Sex | None = Field(default=None, description="Sex of the animal.")
    birth_date: str | None = Field(default=None, description="Birth date (YYYY-MM-DD).")
    create_date: str | None = Field(default=None, description="Case creation date (YYYY-MM-DD).")
    notes: str | None = Field(default=None, description="Additional notes.")
    breed_id: int | None = Field(default=None, description="ID of the breed.")


#######################################################################################################################
# End of file
#######################################################################################################################
