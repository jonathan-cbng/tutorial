#######################################################################################################################
"""
Test suite for the Case CRUD API endpoints.

This module tests the endpoints in backend/routes/case.py:
- POST   /case/      (create a case)
- GET    /case/      (list all cases)
- GET    /case/{id}  (get a case by ID)
- PUT    /case/{id}  (update a case)
- DELETE /case/{id}  (delete a case)

It covers normal and edge cases, including:
- Creating a case (with valid and invalid data)
- Listing cases (empty and after creation)
- Retrieving, updating, and deleting by ID (existing and non-existing)
- Ensuring required foreign keys (breed) are handled
"""
# ruff: noqa: PLR2004
#######################################################################################################################
# Imports
#######################################################################################################################

from fastapi import status
from fastapi.testclient import TestClient

from backend.routes.case import case_field_maps, fuzzy_match_ids
from database.core.models import BreedDbModel

#######################################################################################################################
# Globals
#######################################################################################################################

#######################################################################################################################
# Body
#######################################################################################################################


def case_payload(breed: BreedDbModel) -> dict:
    """Return a dictionary payload for creating a test case with the given breed."""
    return {
        "name": "TestCase",
        "owner": "TestOwner",
        "practice_animal_id": "PA123",
        "chip_id": "CHIP123",
        "breed_id": breed.id,  # Use integer, not str
        "sex": "Male",
        "birth_date": "2020-01-01",
        "create_date": "2025-01-01",
        "notes": "Healthy",
    }


class TestCaseAPI:
    """Test suite for /case endpoints: create, list, retrieve, update, and delete cases."""

    base_url = "/api/case"

    def test_create_case(self, client: TestClient, dog_breed: BreedDbModel) -> None:
        """Test POST /api/case/: Create a case with valid data. Expect 201 and correct response body."""
        payload = case_payload(dog_breed)
        response = client.post(f"{self.base_url}", json=payload)
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        data = response.json()
        assert data["name"] == payload["name"]
        # Check expanded breed object
        assert "breed" in data and isinstance(data["breed"], dict)
        assert data["breed"]["id"] == payload["breed_id"]

    def test_list_cases_empty(self, client: TestClient) -> None:
        """Test GET /case/: List cases when none exist. Expect 200 and empty list."""
        response = client.get(f"{self.base_url}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_cases_after_create(self, client: TestClient, dog_breed: BreedDbModel) -> None:
        """Test GET /case/: List cases after creating one. Expect 200 and list with the created case."""
        payload = case_payload(dog_breed)
        client.post(f"{self.base_url}", json=payload)
        response = client.get(f"{self.base_url}")
        assert response.status_code == status.HTTP_200_OK
        cases = response.json()
        assert len(cases) == 1
        assert cases[0]["name"] == payload["name"]
        # Check expanded breed object in list
        assert "breed" in cases[0] and isinstance(cases[0]["breed"], dict)
        assert cases[0]["breed"]["id"] == payload["breed_id"]

    def test_get_case_by_id(self, client: TestClient, dog_breed: BreedDbModel) -> None:
        """Test GET /case/{id}: Retrieve a case by ID. Expect 200 and correct case data."""
        payload = case_payload(dog_breed)
        post_resp = client.post(f"{self.base_url}", json=payload)
        case_id = post_resp.json()["id"]
        get_resp = client.get(f"{self.base_url}/{case_id}")
        assert get_resp.status_code == status.HTTP_200_OK
        data = get_resp.json()
        assert data["id"] == case_id
        # Check expanded breed object
        assert "breed" in data and isinstance(data["breed"], dict)
        assert data["breed"]["id"] == payload["breed_id"]

    def test_get_case_not_found(self, client: TestClient) -> None:
        """Test GET /case/{id}: Retrieve a non-existent case. Expect 404."""
        random_id = 999999  # Use an integer that won't exist
        response = client.get(f"{self.base_url}/{random_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_case(self, client: TestClient, dog_breed: BreedDbModel) -> None:
        """Test PUT /case/{id}: Update an existing case. Expect 200 and updated data."""
        payload = case_payload(dog_breed)
        post_resp = client.post(f"{self.base_url}", json=payload)
        case_id = post_resp.json()["id"]
        update = {"name": "UpdatedCase"}
        put_resp = client.put(f"{self.base_url}/{case_id}", json={**payload, **update})
        assert put_resp.status_code == status.HTTP_200_OK
        assert put_resp.json()["name"] == "UpdatedCase"

    def test_update_case_not_found(self, client: TestClient, dog_breed: BreedDbModel) -> None:
        """Test PUT /case/{id}: Update a non-existent case. Expect 404."""
        random_id = 999999  # Use an integer that won't exist
        payload = case_payload(dog_breed)
        response = client.put(f"{self.base_url}/{random_id}", json=payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_case(self, client: TestClient, dog_breed: BreedDbModel) -> None:
        """Test DELETE /case/{id}: Delete an existing case. Expect 204, then 404 on retrieval."""
        payload = case_payload(dog_breed)
        post_resp = client.post(f"{self.base_url}", json=payload)
        case_id = post_resp.json()["id"]
        del_resp = client.delete(f"{self.base_url}/{case_id}")
        assert del_resp.status_code == status.HTTP_204_NO_CONTENT
        # Confirm it's gone
        get_resp = client.get(f"{self.base_url}/{case_id}")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_case_not_found(self, client: TestClient) -> None:
        """Test DELETE /case/{id}: Delete a non-existent case. Expect 404."""
        random_id = 999999  # Use an integer that won't exist
        response = client.delete(f"{self.base_url}/{random_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_fuzzy_search_cases(self, client: TestClient, dog_breed: BreedDbModel) -> None:
        """Test GET /case/?fuzzy_match=...: Fuzzy search returns expected cases by name, owner, notes, or breed."""
        # Clear caches to avoid stale data between tests
        fuzzy_match_ids.cache_clear()
        case_field_maps.cache_clear()

        # Create several cases with similar and distinct fields
        payloads = [
            {
                **case_payload(dog_breed),
                "name": "Bella",
                "owner": "Alice",
                "notes": "Healthy",
                "breed_id": dog_breed.id,
            },
            {
                **case_payload(dog_breed),
                "name": "Bellamy",
                "owner": "Alicia",
                "notes": "Sick",
                "breed_id": dog_breed.id,
            },
            {**case_payload(dog_breed), "name": "Max", "owner": "Bob", "notes": "Recovered", "breed_id": dog_breed.id},
        ]
        ids = []
        for p in payloads:
            resp = client.post(f"{self.base_url}", json=p)
            ids.append(resp.json()["id"])

        # Fuzzy search by name (should match both Bella and Bellamy)
        resp = client.get(f"{self.base_url}?fuzzy_match=bell")
        assert resp.status_code == status.HTTP_200_OK
        results = resp.json()
        names = {c["name"] for c in results}
        assert "Bella" in names
        assert "Bellamy" in names
        assert "Max" not in names

        # Fuzzy search by owner (should match Alice and Alicia)
        resp = client.get(f"{self.base_url}?fuzzy_match=alic")
        assert resp.status_code == status.HTTP_200_OK
        owners = {c["owner"] for c in resp.json()}
        assert "Alice" in owners
        assert "Alicia" in owners
        assert "Bob" not in owners

        # Fuzzy search by notes (should match Healthy)
        resp = client.get(f"{self.base_url}?fuzzy_match=healt")
        assert resp.status_code == status.HTTP_200_OK
        notes = {c["notes"] for c in resp.json()}
        assert "Healthy" in notes
        assert "Sick" not in notes

        # Fuzzy search by breed name (should match all, since all use same breed)
        resp = client.get(f"{self.base_url}?fuzzy_match={dog_breed.name[:4]}")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 3

        # Negative test: nonsense query returns empty list
        resp = client.get(f"{self.base_url}?fuzzy_match=zzzzzzzz")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json() == []


#######################################################################################################################
# End of file
#######################################################################################################################
