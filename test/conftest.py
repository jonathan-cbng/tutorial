#######################################################################################################################
"""
Pytest fixtures for test suite.

Provides fixtures for database session, FastAPI app, test client, and test dog breed.
"""

#######################################################################################################################
# Imports
#######################################################################################################################

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel import Session as SQLModelSession

from backend.db import get_session
from backend.db_models import Breed, Case, Species
from main import get_app

#######################################################################################################################
# Globals
#######################################################################################################################

#######################################################################################################################
# Body
#######################################################################################################################


@pytest.fixture
def session() -> Session:
    """Create a new in-memory SQLite session for testing."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with SQLModelSession(engine) as session:
        yield session


@pytest.fixture
def app() -> FastAPI:
    """Return a FastAPI app instance for testing."""
    app = get_app()
    return app


@pytest.fixture
def client(session, monkeypatch) -> TestClient:
    """Return a TestClient using the test session and monkeypatched get_session."""

    def get_session_override():
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()

    monkeypatch.setattr("main.get_session", get_session_override)
    app = get_app()
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
        app.dependency_overrides.clear()


@pytest.fixture
def dog_breed(session: Session) -> Breed:
    """Create and return a test dog breed in the test session."""
    breed = Breed(name="TestBreed", species=Species.CANINE)
    return breed.create(session)


@pytest.fixture
def empty_case(session, dog_breed: Breed) -> Case:
    """
    Fixture to create a test case for panel tests.

    Args:
    ----
        session: The database session.
        dog_breed (Breed): The breed to assign to the case.

    Returns:
    -------
        Case: The created Case instance.

    """
    case = Case(
        name="PanelCase",
        owner="Owner",
        practice_animal_id="PA456",
        chip_id="CHIP456",
        breed_id=dog_breed.id,
        sex="Female",
        birth_date="2021-01-01",
        create_date="2025-01-02",
        notes="Case for panel",
    )
    return case.create(session)


@pytest.fixture
def another_case(session, dog_breed: Breed) -> Case:
    """Fixture to create a second test case for panel filtering tests."""
    case = Case(
        name="AnotherPanelCase",
        owner="AnotherOwner",
        practice_animal_id="PA789",
        chip_id="CHIP789",
        breed_id=dog_breed.id,
        sex="Male",
        birth_date="2020-05-05",
        create_date="2025-02-02",
        notes="Another case for panel filtering",
    )
    return case.create(session)


#######################################################################################################################
# End of file
#######################################################################################################################
