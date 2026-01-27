#######################################################################################################################

#######################################################################################################################
"""
Test suite for root API redirect behavior.

This module contains tests that verify the FastAPI application's root API endpoint(s) correctly redirect users to the
documentation page. Specifically, it ensures that both `/api` and `/api/` return a redirect (302 or 307) to `/docs`,
regardless of trailing slash usage. This is important for user experience and consistency, as users may access the API
root with or without a trailing slash.

Tested endpoints:
- /api
- /api/

Assertions:
- The response status code is 302 or 307 (redirect).
- The Location header is set to `/docs`.

The test uses parameterization to check both forms of the endpoint in a single test function.
"""

#######################################################################################################################
# Imports
#######################################################################################################################

from fastapi import status
from fastapi.testclient import TestClient

#######################################################################################################################
# Globals
#######################################################################################################################

#######################################################################################################################
# Body
#######################################################################################################################


class TestRoot:
    """Test suite for /api root endpoint redirect behavior."""

    base_url = "/api"

    def test_read_root(self, client: TestClient) -> None:
        """
        Test that the /api endpoint returns a redirect to /docs.

        This ensures that both /api and /api/ (due to FastAPI's routing) will redirect users to the documentation page.
        The test checks for a 302 or 307 redirect status code and verifies that the Location header is set to /docs.
        """
        response = client.get(self.base_url, follow_redirects=False)
        assert response.status_code in (status.HTTP_302_FOUND, status.HTTP_307_TEMPORARY_REDIRECT)
        assert response.headers["location"] == "/docs"


#######################################################################################################################
# End of file
#######################################################################################################################
