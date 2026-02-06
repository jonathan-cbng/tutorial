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

import asyncio

#######################################################################################################################
# Imports
#######################################################################################################################
from cachetools import TTLCache, cached
from rapidfuzz import process

from database.core.models import Case
from database.core.session import needs_session

#######################################################################################################################
# Globals
#######################################################################################################################

CACHE_SIZE = 128
REFRESH_INTERVAL = 5  # Number of seconds between cache refreshes

#######################################################################################################################
# Body
#######################################################################################################################


class FuzzyMatchService:
    """Service for fuzzy matching clinical cases."""

    def __init__(self):
        """Initialise the fuzzy match service with an empty mapping."""
        self._map = {}

    async def reset(self):
        """Clear the fuzzy match cache and refresh the mapping."""
        await self.refresh()
        self.fuzzy_match_ids.cache_clear()

    @needs_session
    async def refresh(self, session):
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

        self._map = field_map

    async def refresh_loop(self):
        """
        Perform a periodic refresh operations in an asynchronous loop.

        The method repeatedly calls the `refresh` coroutine at an interval defined by
        the `_refresh_interval` attribute. This loop will continue running indefinitely.
        """
        while True:
            await self.refresh()
            await asyncio.sleep(REFRESH_INTERVAL)

    @cached(cache=TTLCache(maxsize=CACHE_SIZE, ttl=REFRESH_INTERVAL / 2))
    def fuzzy_match_ids(self, query: str, min_match_score: int) -> list[int]:
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
        results = [
            (case_id, process.extractOne(query.lower(), fields, score_cutoff=min_match_score))
            for case_id, fields in self._map.items()
        ]
        results = [r for r in results if r[1] is not None]  # filter out non-matches
        results = sorted(results, key=lambda r: r[1][1], reverse=True)  # sort by score
        sorted_ids = [r[0] for r in results]

        return sorted_ids


fuzzy_match_service = FuzzyMatchService()

#######################################################################################################################
# End of file
#######################################################################################################################
