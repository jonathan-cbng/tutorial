#######################################################################################################################
"""
Test suite for the /breeds endpoints.

Covers:
- Listing all breeds
- Filtering breeds by species
- Retrieving breeds by ID and name
- Handling not found cases
"""

#######################################################################################################################
# Imports
#######################################################################################################################

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, select

from backend.database.models import BreedDbModel
from backend.static_data.breeds.canine import DOG_BREEDS
from backend.static_data.breeds.equine import HORSE_BREEDS
from backend.static_data.breeds.feline import CAT_BREEDS

#######################################################################################################################
# Globals
#######################################################################################################################

#######################################################################################################################
# Body
#######################################################################################################################


class TestBreedAPI:
    """Test suite for /breeds endpoints."""

    base_url = "/api/breed"

    def test_list_breeds(self, client: TestClient) -> None:
        """Test GET /api/breeds/ returns all breeds in the database."""
        resp = client.get(f"{self.base_url}")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        breeds = {b["name"] for b in data}
        assert DOG_BREEDS[0] in breeds
        assert len(data) == len(DOG_BREEDS) + len(CAT_BREEDS) + len(HORSE_BREEDS)

    def test_list_breeds_species_filter(self, client: TestClient) -> None:
        """Test GET /api/breeds/?species=... filters breeds by species."""
        resp = client.get(f"{self.base_url}?species=Canine")
        assert resp.status_code == status.HTTP_200_OK, resp.json()
        data = resp.json()
        species = {b["species"] for b in data}
        assert "Canine" in species
        assert DOG_BREEDS[0] in {b["name"] for b in data}
        assert len(data) == len(DOG_BREEDS)

    def test_get_breed_by_id(self, client: TestClient, session: SQLModel) -> None:
        """Test GET /api/breeds/{id} returns the correct breed by ID."""
        breed = session.exec(select(BreedDbModel).where(BreedDbModel.name == DOG_BREEDS[0])).first()
        assert breed is not None
        resp = client.get(f"{self.base_url}/{breed.id}")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["name"] == DOG_BREEDS[0]

    def test_get_breed_not_found(self, client: TestClient) -> None:
        """Test GET /api/breeds/{id} returns 404 for a non-existent breed."""
        resp = client.get(f"{self.base_url}/999999")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_get_breed_by_name(self, client: TestClient) -> None:
        """
        Test GET /api/breeds/by_name/{breed_name}.

        Tests that it returns the correct breed by name and 404 for non-existent breed.
        """
        resp = client.get(f"{self.base_url}/by_name/{DOG_BREEDS[0]}")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["name"] == DOG_BREEDS[0]
        # Test valid breed name with species filter
        resp = client.get(f"{self.base_url}/by_name/{DOG_BREEDS[0]}?species=Canine")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["name"] == DOG_BREEDS[0]
        # Test non-existent breed name
        resp = client.get(f"{self.base_url}/by_name/NotARealBreed")
        assert resp.status_code == status.HTTP_404_NOT_FOUND


#######################################################################################################################
# End of file
#######################################################################################################################
