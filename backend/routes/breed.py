#######################################################################################################################
"""
Breed API routes for backend.

This module defines endpoints for retrieving breed data:

- GET /breeds/:
    List all breeds. Supports optional filtering by species via the 'species' query parameter.
- GET /breeds/{breed_id}:
    Retrieve a single breed by its ID. Supports optional filtering by species via the 'species' query parameter.
- GET /breeds/by_name/{breed_name}:
    Retrieve a single breed by its name. Supports optional filtering by species via the 'species' query parameter.

All endpoints use SQLModel for ORM access and FastAPI dependency injection for database sessions.
"""

#######################################################################################################################
# Imports
#######################################################################################################################

from fastapi import APIRouter, Depends, Path, Query
from sqlmodel import Session, select

from backend.database.models import BreedDbModel, Species
from backend.database.session import get_session

#######################################################################################################################
# Globals
#######################################################################################################################

breed_router = APIRouter()

#######################################################################################################################
# Body
#######################################################################################################################


@breed_router.get(
    "",  # Explicitly set path to /breeds/
    summary="List all breeds",
    description="List all breeds, optionally filtered by species.",
)
def list_breeds(
    species: Species | None = Query(None, description="Filter by species"),
    session: Session = Depends(get_session),
) -> list[BreedDbModel]:
    """
    List all breeds, optionally filtered by species.

    Args:
    ----
        species (Species | None): Optional species filter.
        session (Session): Database session.

    Returns:
    -------
        list[Breed]: List of breeds.

    """
    query = select(BreedDbModel).order_by(BreedDbModel.name)
    if species:
        query = query.where(BreedDbModel.species == species)
    return list(session.exec(query).all())


@breed_router.get(
    "/{breed_id}",
    summary="Retrieve a breed by ID",
    description="Retrieve a breed by ID.",
)
def get_breed_by_id(
    breed_id: int = Path(..., description="The breed's ID"),
    session: Session = Depends(get_session),
) -> BreedDbModel:
    """
    Retrieve a breed by ID.

    Args:
    ----
        breed_id (int): The breed's ID.
        session (Session): Database session.

    Returns:
    -------
        Breed: The breed object.

    """
    return BreedDbModel.get_by_id_or_404(session, breed_id)


@breed_router.get(
    "/by_name/{breed_name}",
    summary="Retrieve a breed by name",
    description="Retrieve a breed by name.",
)
def get_breed_by_name(
    breed_name: str = Path(..., description="The breed's name"),
    session: Session = Depends(get_session),
) -> BreedDbModel:
    """
    Retrieve a breed by name.

    Args:
    ----
        breed_name (str): The breed's name.
        session (Session): Database session.

    Returns:
    -------
        Breed: The breed object.

    """
    return BreedDbModel.get_by_name_or_404(session, breed_name)


#######################################################################################################################
# End of file
#######################################################################################################################
