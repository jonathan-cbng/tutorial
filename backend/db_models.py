#######################################################################################################################
"""
Database ORM models and enums for the backend.

Contains all SQLModel ORM models (table=True), enums, and mixins used for database tables.
"""

# Ignore None comparison warning for SQLAlchemy
#######################################################################################################################
# Imports
#######################################################################################################################
from collections.abc import Iterable
from enum import Enum

from fastapi import HTTPException
from sqlalchemy import ColumnElement
from sqlalchemy.orm import selectinload
from sqlmodel import Field, Relationship, Session, SQLModel, and_, select

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


# Helper Mixin classes
class DbHelperMixin:
    """Mixin providing common database helper methods for database models."""

    @classmethod
    def get_by_id_or_404(
        cls, session: Session, id, greedy_fields: Iterable[str] = tuple(), additional_filters: Iterable = tuple()
    ):
        """
        Get an object by its ID or raise 404 if not found.

        Args:
        ----
            session: The database session to use for the query.
            id: The primary key value to search for.
            greedy_fields: Iterable of related fields to eagerly load.
            additional_filters: Iterable of additional SQLAlchemy filter expressions to apply.

        Returns:
        -------
            The object instance if found.

        Raises:
        ------
            HTTPException: If the object is not found.

        """
        stmt = select(cls).where(cls.id == id)
        if additional_filters:
            stmt = stmt.where(and_(*additional_filters))
        for field in greedy_fields:
            stmt = stmt.options(selectinload(getattr(cls, field)))
        obj = session.exec(stmt).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{cls.__name__} not found")
        return obj

    @classmethod
    def get_by_name_or_404(
        cls, session: Session, name, greedy_fields: Iterable[str] = tuple(), additional_filters: Iterable = tuple()
    ):
        """
        Get an object by its name or raise 404 if not found.

        Args:
        ----
            session: The database session to use for the query.
            name: The name value to search for.
            greedy_fields: Iterable of related fields to eagerly load.
            additional_filters: Iterable of additional SQLAlchemy filter expressions to apply.

        Returns:
        -------
            The object instance if found.

        Raises:
        ------
            HTTPException: If the object is not found.

        """
        stmt = select(cls).where(cls.name == name)
        if additional_filters:
            stmt = stmt.where(and_(*additional_filters))
        for field in greedy_fields:
            stmt = stmt.options(selectinload(getattr(cls, field)))
        obj = session.exec(stmt).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{cls.__name__} not found")
        return obj

    @classmethod
    def get_all(
        cls,
        session: Session,
        greedy_fields: Iterable[str] = tuple(),
        additional_filters: Iterable = tuple(),
        sort_field: ColumnElement = None,
    ):
        """
        Get all objects of this class from the database.

        Args:
        ----
            session: The database session to use for the query.
            greedy_fields: Iterable of related fields to eagerly load.
            additional_filters: Iterable of additional SQLAlchemy filter expressions to apply.
            sort_field: Optional field to sort the results by (should be a SQLModel field).

        Returns:
        -------
            List of all object instances of this class.

        """
        stmt = select(cls)
        if additional_filters:
            stmt = stmt.where(and_(*additional_filters))
        if sort_field:
            stmt = stmt.order_by(sort_field)
        for field in greedy_fields:
            stmt = stmt.options(selectinload(getattr(cls, field)))
        return session.exec(stmt).all()

    def create(self, session):
        """
        Add and flush a new object to the database.

        Args:
        ----
            session: The database session to use for the operation.

        Returns:
        -------
            The added and refreshed object instance.

        """
        session.add(self)
        session.flush()
        session.refresh(self)
        return self

    def update(self, session: Session, update_data: dict | object):
        """
        Update an object with new data and flush changes.

        Args:
        ----
            session: The database session to use for the operation.
            update_data: A dict or object containing updated fields and values.

        Returns:
        -------
            The updated and refreshed object instance.

        """
        if hasattr(update_data, "model_dump"):
            update_data = update_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(self, key, value)
        session.add(self)
        session.flush()
        session.refresh(self)
        return self

    def delete(self, session) -> None:
        """
        Delete an object from the database and flush changes.

        Args:
        ----
            session: The database session to use for the operation.

        """
        session.delete(self)
        session.flush()


# Breed
class Breed(DbHelperMixin, SQLModel, table=True):
    """Database model for animal breeds."""

    __tablename__ = "breed"
    id: int = Field(default=None, primary_key=True, index=True, description="Breed ID.")
    name: str = Field(index=True, nullable=False, max_length=NAME_LENGTH, description="Breed name.")
    species: Species = Field(index=True, description="Species this breed belongs to.")


# Case
class Case(DbHelperMixin, SQLModel, table=True):
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
