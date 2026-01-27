#######################################################################################################################
"""
Test suite for the Species API endpoint.

This module tests the endpoint in backend/routes/species.py:
- GET /species/ (list all species)

It covers normal and edge cases, including:
- Listing all available species
"""

#######################################################################################################################
# Imports
#######################################################################################################################

from fastapi import status
from fastapi.testclient import TestClient

from backend.db_models import Species

#######################################################################################################################
# Body
#######################################################################################################################


class TestSpeciesAPI:
    """Test suite for /species endpoint: list all species."""

    base_url = "/api/species"

    def test_get_species(self, client: TestClient) -> None:
        """Test GET /api/species/: List all species. Expect 200 and correct values."""
        response = client.get(f"{self.base_url}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        expected = [s.value for s in Species]
        assert set(data) == set(expected)
        assert len(data) == len(expected)


#######################################################################################################################
# End of file
#######################################################################################################################
