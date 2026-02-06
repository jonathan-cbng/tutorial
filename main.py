#!/usr/bin/env python
#######################################################################################################################
"""
Main entry point for the FastAPI application.

This module defines the FastAPI app factory, registers all API routers, and attaches the application lifespan logic.
Run this file directly to start the application with Uvicorn.

- Defines get_app(), which creates and configures the FastAPI app.
- Registers all API routers (root, case, breed).
- Attaches the lifespan context manager from backend.app.
- Runs the app with Uvicorn if executed as __main__.
"""

#######################################################################################################################
# Imports
#######################################################################################################################

import asyncio
import threading
import time
import webbrowser
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.api import api_router, tags_metadata
from services.fuzzy import fuzzy_match_service
from services.static_data.breeds import ensure_cat_breeds, ensure_dog_breeds, ensure_horse_breeds

#######################################################################################################################
# Globals
#######################################################################################################################

DEFAULT_PORT = 8000
STARTUP_WAIT = 0.1  # seconds

#######################################################################################################################
# Body
#######################################################################################################################


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager for FastAPI.

    Ensures that all standard dog, cat, and horse breeds and panel types are present in the database at application
    startup.
    """
    ensure_dog_breeds()
    ensure_cat_breeds()
    ensure_horse_breeds()

    # Start fuzzy match refresh loop
    refresh_task = asyncio.create_task(fuzzy_match_service.refresh_loop())
    app.setup_complete = True

    yield

    # Cancel refresh loop on shutdown
    refresh_task.cancel()
    try:
        await refresh_task
    except asyncio.CancelledError:
        pass


def get_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Sets up the application with all API routers and the lifespan context manager.
    Returns the configured FastAPI app instance.
    """
    app = FastAPI(lifespan=lifespan, openapi_tags=tags_metadata)
    app.include_router(api_router, prefix="/api")
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
    return app


app = get_app()
app.setup_complete = False

#######################################################################################################################
# Entry Point
#######################################################################################################################

if __name__ == "__main__":

    def run():
        """
        Run the FastAPI application with Uvicorn.

        This never returns, so it is run in a separate thread so we can open the browser once the server is ready.
        :return:
        """
        uvicorn.run(app, port=8000)

    threading.Thread(target=run, daemon=True).start()
    while not app.setup_complete:
        time.sleep(0.1)
    webbrowser.open("http://localhost:8000")
    threading.Event().wait()


#######################################################################################################################
# End of file
#######################################################################################################################
