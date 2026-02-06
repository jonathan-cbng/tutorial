from unittest.mock import patch

import pytest
from fastapi import HTTPException
from sqlmodel import Session, select
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from database.core.models import BreedDbModel, CaseDbModel, Species


class TestSessionManagement:
    """
    Class for testing session management in API calls.

    This class contains tests to ensure proper handling of database
    sessions within API endpoints. It verifies that database changes
    are appropriately committed or rolled back based on the outcome
    of API calls. These tests ensure that transactions are handled
    correctly during both successful and exceptional flows, guarding
    against data inconsistencies in the database.

    Methods:
        test_api_get_session_commit: Tests if database changes are committed
            after a successful API call to create a case.
        test_api_get_session_http_exception_commit: Verifies that database
            changes are committed even when an HTTPException is raised.
        test_api_get_session_rollback: Ensures that database changes are
            rolled back in case of a general exception.

    """

    def test_api_get_session_commit(self, client, session, dog_breed):
        """Test that get_session commits on successful API call to create_case."""
        case_data = {"name": "ApiCommitCase", "breed_id": dog_breed.id, "owner": "Owner", "sex": "Male"}
        response = client.post("/api/case", json=case_data)
        assert response.status_code == HTTP_201_CREATED

        # Check if it was committed
        with Session(session.bind) as check_session:
            statement = select(CaseDbModel).where(CaseDbModel.name == "ApiCommitCase")
            results = check_session.exec(statement).all()
            assert len(results) == 1

    def test_api_get_session_http_exception_commit(self, client, session, dog_breed):
        """Test that get_session commits even when API raises HTTPException."""
        # We want to verify that if something was added to the session,
        # and then an HTTPException is raised, it is COMMITTED.

        # We'll use a side effect that adds a breed to the session then raises HTTPException.
        def add_and_raise(s):
            breed = BreedDbModel(name="ApiHttpBreed", species=Species.CANINE)
            s.add(breed)
            s.flush()  # Ensure it's in the session's pending changes
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Test Error")

        with patch("backend.routes.case.CaseDbModel.create", side_effect=add_and_raise):
            case_data = {
                "name": "Dummy",
                "breed_id": dog_breed.id,
            }
            response = client.post("/api/case", json=case_data)
            assert response.status_code == HTTP_400_BAD_REQUEST

        # Check if ApiHttpBreed was committed
        with Session(session.bind) as check_session:
            statement = select(BreedDbModel).where(BreedDbModel.name == "ApiHttpBreed")
            results = check_session.exec(statement).all()
            assert len(results) == 1

    def test_api_get_session_rollback(self, client, session, dog_breed):
        """Test that get_session rolls back when API raises a general Exception."""

        def add_and_raise_val_error(s):
            breed = BreedDbModel(name="ApiRollbackBreed", species=Species.CANINE)
            s.add(breed)
            s.flush()
            raise ValueError("Test Exception")

        with patch("backend.routes.case.CaseDbModel.create", side_effect=add_and_raise_val_error):
            case_data = {
                "name": "Dummy",
                "breed_id": dog_breed.id,
            }
            with pytest.raises(ValueError):
                client.post("/api/case", json=case_data)

        # Check if ApiRollbackBreed was NOT committed
        with Session(session.bind) as check_session:
            statement = select(BreedDbModel).where(BreedDbModel.name == "ApiRollbackBreed")
            results = check_session.exec(statement).all()
            assert len(results) == 0
