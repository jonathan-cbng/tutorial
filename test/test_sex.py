#######################################################################################################################
"""
Test suite for the SexEnum API endpoint.

This module tests the endpoint in backend/routes/sex.py:
- GET /sex/ (list all sexes)

It covers normal and edge cases, including:
- Listing all available sexes
"""

#######################################################################################################################
# Imports
#######################################################################################################################

from fastapi import status
from fastapi.testclient import TestClient

from database.core.models import Sex

#######################################################################################################################
# Globals
#######################################################################################################################

#######################################################################################################################
# Body
#######################################################################################################################


class TestSexAPI:
    """Test suite for /sex endpoint: list all sexes."""

    base_url = "/api/sex"

    def test_get_sexes(self, client: TestClient) -> None:
        """Test GET /api/sex/: List all sexes. Expect 200 and correct values."""
        response = client.get(f"{self.base_url}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        expected = {sex.value for sex in Sex}
        assert set(data) == expected
        assert len(data) == len(expected)


#######################################################################################################################
# End of file
#######################################################################################################################
