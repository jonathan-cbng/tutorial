#######################################################################################################################
"""
Case API routes.

This module defines endpoints for creating, retrieving, updating, and deleting clinical cases:

- POST /case/:
    Create a new case. Accepts a CaseCreate payload and returns the created case.
- GET /case/:
    List all cases. Returns a list of CaseRead objects.
- GET /case/{case_id}:
    Retrieve a single case by its ID. Returns a CaseRead object or 404 if not found.
- PUT /case/{case_id}:
    Update an existing case by its ID. Accepts a CaseUpdate payload and returns the updated case, or 404 if not found.
- DELETE /case/{case_id}:
    Delete a case by its ID. Returns 204 on success or 404 if not found.

All endpoints use SQLModel for ORM access and FastAPI dependency injection for database sessions.
"""

#######################################################################################################################
# Imports
#######################################################################################################################

from cachetools import LRUCache, TTLCache, cached
from fastapi import APIRouter, Depends, Query, status
from rapidfuzz import process
from sqlmodel import Session

from backend.api_models import CaseCreate, CaseRead, CaseUpdate
from backend.db import get_session
from backend.db_models import Case

#######################################################################################################################
# Globals
#######################################################################################################################

CACHE_SIZE = 128
CACHE_TTL = 300  # seconds
case_router = APIRouter()


#######################################################################################################################
# Body
#######################################################################################################################


@cached(cache=TTLCache(maxsize=1, ttl=CACHE_TTL), key=lambda session: ())
def case_field_maps(session: Session) -> dict[int, list[str]]:
    """
    Create a mapping of searchable fields to cases for fuzzy searching.

    Args:
    ----
        session (Session): The database session.

    Returns:
    -------
        dict[int, list[str]]: Mapping from case ID to list of searchable strings.

    """
    cases = Case.get_all(session, greedy_fields=["breed"])
    field_map = {}
    for case in cases:
        strings = []
        if case.name:
            strings.append(case.name.lower())
        if case.owner:
            strings.append(case.owner.lower())
        if case.notes:
            strings.append(case.notes.lower())
        if case.breed:
            strings.append(case.breed.name.lower())
        field_map[case.id] = strings

    return field_map


@cached(cache=LRUCache(maxsize=CACHE_SIZE), key=lambda query, limit, session: (query, limit))
def fuzzy_match_ids(query: str, min_match_score: int, session: Session) -> list[int]:
    """
    Perform a fuzzy search for cases based on the query string.

    Args:
    ----
        query (str): String to search for.
        min_match_score (int): Cutoff matching score below which fuzzy matching does not report a case.
        session (Session): The database session.

    Returns:
    -------
        list[int]: The case IDs that best match the query in descending order of match quality.

    """
    field_map = case_field_maps(session)  # This is a dictioary of case_id -> list of strings to search
    results = [
        (case_id, process.extractOne(query, fields, score_cutoff=min_match_score))
        for case_id, fields in field_map.items()
    ]
    results = [r for r in results if r[1] is not None]  # filter out non-matches
    results = sorted(results, key=lambda r: r[1][1], reverse=True)  # sort by score
    sorted_ids = [r[0] for r in results]

    return sorted_ids


@case_router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(case: CaseCreate, session: Session = Depends(get_session)):
    """Create a new clinical case."""
    case = Case.model_validate(case)
    return case.create(session)


@case_router.get(
    "",
    response_model=list[CaseRead],
    summary="List all clinical cases",
    description="List all clinical cases. Optionally filter by fuzzy search on name, owner, notes, or breed.",
)
def list_cases(
    session: Session = Depends(get_session),
    fuzzy_match: str | None = Query(
        default=None, description="Fuzzy search string to match against case name, owner, notes, or breed."
    ),
    min_match_score: int | None = Query(
        default=60,
        description="Cutoff matching score below which fuzzy matching does not report a case.",
    ),
):
    """
    List all clinical cases.

    Args:
    ----
        session (Session): The database session.
        fuzzy_match (str | None): Optional fuzzy search string.
        min_match_score (int | None): Cutoff matching score below which fuzzy matching does not report a case.

    Returns:
    -------
        list[CaseRead]: List of cases matching the criteria.

    """
    filter = (Case.id.in_(fuzzy_match_ids(fuzzy_match, min_match_score, session)),) if fuzzy_match else None
    return Case.get_all(session, greedy_fields=["breed"], additional_filters=filter)


@case_router.get("/{case_id}", response_model=CaseRead)
def get_case(case_id: int, session: Session = Depends(get_session)):
    """Retrieve a clinical case by ID."""
    return Case.get_by_id_or_404(session, case_id, greedy_fields=["breed"])


@case_router.put("/{case_id}", response_model=CaseRead)
def update_case(case_id: int, case_data: CaseUpdate, session: Session = Depends(get_session)):
    """Update a clinical case by ID."""
    db_case = Case.get_by_id_or_404(session, case_id)
    return db_case.update(session, case_data)


@case_router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(case_id: int, session: Session = Depends(get_session)):
    """Delete a clinical case by ID."""
    db_case = Case.get_by_id_or_404(session, case_id)
    session.delete(db_case)
    session.commit()


#######################################################################################################################
# End of file
#######################################################################################################################
