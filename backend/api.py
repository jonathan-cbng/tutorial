#######################################################################################################################
"""
API router and root redirect logic for the FastAPI application.

This module provides the main API router, includes all route modules, and defines the root redirect to /docs.
Note: This file does not define the FastAPI app itself; see main.py for the app factory and route registration.
"""

#######################################################################################################################
# Imports
#######################################################################################################################

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from backend.routes.breed import breed_router
from backend.routes.case import case_router
from backend.routes.sex import sex_router
from backend.routes.species import species_router

#######################################################################################################################
# Globals
#######################################################################################################################

api_router = APIRouter()

# OpenAPI tags metadata for documentation grouping

tags_metadata = [
    {
        "name": "Animal Information",
        "description": "Read-only endpoints for animal-related reference data (species, breeds, sex).",
    },
    {"name": "Cases", "description": "Endpoints for clinical case management."},
    {"name": "Panels", "description": "Endpoints to create and manipulate laboratory panels and measurements."},
    {"name": "Analysis", "description": "Endpoints for analysis management."},
]

#######################################################################################################################
# Body
#######################################################################################################################


@api_router.get("", include_in_schema=False)
def redirect_to_documentation() -> RedirectResponse:
    """Redirects to the /docs page for API information."""
    return RedirectResponse(url="/docs")


api_router.include_router(breed_router, prefix="/breed", tags=["Animal Information"])
api_router.include_router(sex_router, prefix="/sex", tags=["Animal Information"])
api_router.include_router(species_router, prefix="/species", tags=["Animal Information"])
api_router.include_router(case_router, prefix="/case", tags=["Cases"])

#######################################################################################################################
# End of file
#######################################################################################################################
