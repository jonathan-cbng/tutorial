#######################################################################################################################
"""
Database setup and session management for the backend.

- Creates the SQLAlchemy engine using the configured DATABASE_URL.
- Ensures SQLite foreign key enforcement if using SQLite.
- Provides a session generator for dependency injection.
"""

from functools import wraps

from fastapi import HTTPException

#######################################################################################################################
# Imports
#######################################################################################################################
from sqlalchemy import create_engine, event
from sqlmodel import Session

from backend.config import config

#######################################################################################################################
# Globals
#######################################################################################################################

engine = create_engine(config.DATABASE_URL)  # Set echo=True for lots of debug output

#######################################################################################################################
# Body
#######################################################################################################################


def _enable_sqlite_foreign_keys(dbapi_con, con_record):
    """
    Enable foreign key enforcement for SQLite connections.

    Called automatically by SQLAlchemy event system on connect.
    """
    dbapi_con.execute("PRAGMA foreign_keys=ON")


def get_session():
    """
    Dependency generator that yields a SQLModel Session bound to the app engine.

    Usage: `Depends(get_session)` in FastAPI endpoints.
    Ensures rollback on uncaught exceptions (except HTTPException), otherwise commits.
    """
    with Session(engine) as session:
        try:
            yield session
        except HTTPException:
            session.commit()
            raise
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()


def needs_session(func):
    """
    Decorate to provide a SQLmodel session to the decorated function.

    The session is created, closed and committed automatically.

    Usage:
        @needs_session
        def some_function(session: Session):
            # perform database operations with db
            ...

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "session" in kwargs:
            return func(*args, **kwargs)
        else:
            with Session(engine) as session:
                try:
                    result = func(*args, session=session, **kwargs)
                except HTTPException:
                    session.commit()
                    raise
                except Exception:
                    session.rollback()
                    raise
                else:
                    session.commit()
                return result

    return wrapper


if config.DATABASE_URL.startswith("sqlite"):
    # Enable foreign key enforcement for SQLite
    event.listen(engine, "connect", _enable_sqlite_foreign_keys)

#######################################################################################################################
# End of file
#######################################################################################################################
