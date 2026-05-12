"""User story test for US-05: empty input error handling."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from myproject.api import app
from myproject.router import route_query


@pytest.mark.user_story("US-05")
def test_us_05_empty_input_router_error() -> None:
    """Given/When/Then.

    Given the Adaptive RAG application pipeline is available,
    When the user submits an empty question to the router,
    Then the router raises a clear input text is required error.
    """
    with pytest.raises(ValueError, match="input text is required"):
        route_query("")


@pytest.mark.user_story("US-05")
def test_us_05_empty_input_api_error() -> None:
    """Given/When/Then.

    Given the Adaptive RAG API is available,
    When the user submits an empty question to POST /api/query,
    Then the API returns HTTP 400 with the error input text is required.
    """
    client = TestClient(app)

    response = client.post(
        "/api/query",
        json={"text": "", "max_results": 5},
    )

    assert response.status_code == 400
    assert response.json() == {"error": "input text is required"}
