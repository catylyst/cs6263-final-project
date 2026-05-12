"""Fast API server for the Adaptive RAG project."""

from __future__ import (
    annotations,  # library that allows for postponed evaluation of type annotations
)

from fastapi import (  # FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
    FastAPI,
    HTTPException,
)
from fastapi.responses import (
    JSONResponse,  # JSONResponse is a class in FastAPI that allows you to return JSON responses from your API endpoints.
)

from myproject.router import (
    route_query,  # Importing the route_query function from the router module in the myproject package.
)
from myproject.schemas import (  # Importing the ErrorResponse, QueryRequest, and QueryResponse classes from the schemas module in the myproject package.
    ErrorResponse,
    QueryRequest,
    QueryResponse,
)

app = FastAPI(  # Creating an instance of the FastAPI class, which will be used to define the API endpoints and their behavior.
    title="Adaptive RAG Question Answering System",
    description=(
        "A simplified Adaptive RAG system that routes questions to no retrieval, "
        "single-step retrieval, or multi-step retrieval based on question complexity."
    ),
    version="0.1.0",
)  # This instance of FastAPI is configured with a title, description, and version, which will be used in the automatically generated API documentation provided by FastAPI.


@app.get("/")  # This is a decorator that defines a GET endpoint at the root URL ("/") of the API.
def home() -> (
    dict
):  # This function defines the logic for handling GET requests to the root URL ("/") of the API. It returns a dictionary with information about the API, including its name, status, and the endpoint for querying.
    """Health and project information endpoint."""
    return {
        "name": "Adaptive RAG Question Answering System",
        "status": "running",
        "query_endpoint": "/api/query",
    }  # This function returns a dictionary with information about the API, including its name, status, and the endpoint for querying.


@app.get(
    "/health"
)  # This is a decorator that defines a GET endpoint at the "/health" URL of the API.
def health() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
    }  # This function returns a dictionary indicating that the API is healthy.


@app.post(
    "/api/query",  # This is a decorator that defines a POST endpoint at the "/api/query" URL of the API.
    response_model=QueryResponse,  # This specifies that the response from this endpoint will be of type QueryResponse.
    responses={
        400: {
            "model": ErrorResponse
        },  # This specifies that if the endpoint returns a 400 status code, the response will be of type ErrorResponse.
    },
)
def query(
    request: QueryRequest,
) -> (
    QueryResponse
):  # This function defines the logic for handling POST requests to the "/api/query" endpoint. It takes a QueryRequest object as input and returns a QueryResponse object.
    """Answer a user question using adaptive retrieval routing."""
    try:  # The try block is used to catch any ValueError exceptions that may occur during the execution of the route_query function.
        result = route_query(  # The route_query function is called with the text and max_results from the request. It processes the query and returns a result.
            text=request.text,  # The text of the query that the user wants to ask.
            max_results=request.max_results,  # The maximum number of results that the user wants to receive in the response.
        )
        return QueryResponse(
            **result
        )  # The result from the route_query function is unpacked and used to create a QueryResponse object, which is then returned as the response to the API request.

    except (
        ValueError
    ) as exc:  # If a ValueError exception is raised during the execution of the try block, it is caught here and handled.
        message = str(
            exc
        )  # The error message from the exception is converted to a string and stored in the variable 'message'.

        if (
            message
            in {  # If the error message is either "input text is required" or "input text exceeds maximum length", a 400 HTTPException is raised with the error message included in the response.
                "input text is required",
                "input text exceeds maximum length",
            }
        ):
            raise HTTPException(
                status_code=400, detail={"error": message}
            ) from exc  # If the error message does not match the specified messages, a generic 400 HTTPException is raised with a default error message indicating that the request failed.

        raise HTTPException(
            status_code=400, detail={"error": message}
        ) from exc  # If the error message does not match the specified messages, a generic 400 HTTPException is raised with a default error message indicating that the request failed.


@app.exception_handler(
    HTTPException
)  # This is a decorator that registers a custom exception handler for HTTPException. When an HTTPException is raised in the application, this handler will be called to generate a response.
def http_exception_handler(
    _: object, exc: HTTPException
) -> (
    JSONResponse
):  # This function defines the logic for handling HTTPException errors. It takes the exception as input and returns a JSONResponse object that contains the error message in a format that is compatible with the project specifications.
    """Return rubric-friendly error responses.

    FastAPI normally wraps errors as {"detail": ...}. The project SPEC expects
    {"error": "..."} for validation and user-story error tests.
    """
    detail = (
        exc.detail
    )  # The detail attribute of the HTTPException contains the error message or information about the error that occurred.

    if (
        isinstance(detail, dict) and "error" in detail
    ):  # If the detail is a dictionary and contains the key "error", a JSONResponse is returned with the error message extracted from the detail dictionary.
        return JSONResponse(  # A JSONResponse is returned with the status code from the exception and the error message extracted from the detail dictionary.
            status_code=exc.status_code,  # The HTTP status code from the exception is used as the status code for the response.
            content={
                "error": detail["error"]
            },  # The error message is extracted from the detail dictionary and included in the response content under the key "error".
        )

    if isinstance(
        detail, str
    ):  # If the detail is a string, a JSONResponse is returned with the error message included in the response content under the key "error".
        return JSONResponse(  # A JSONResponse is returned with the status code from the exception and the error message included in the response content under the key "error".
            status_code=exc.status_code,  # The HTTP status code from the exception is used as the status code for the response.
            content={
                "error": detail
            },  # The error message from the detail string is included in the response content under the key "error".
        )

    return JSONResponse(  # If the detail is neither a dictionary with an "error" key nor a string, a generic JSONResponse is returned with a default error message indicating that the request failed.
        status_code=exc.status_code,  # The HTTP status code from the exception is used as the status code for the response.
        content={
            "error": "request failed"
        },  # A default error message is included in the response content under the key "error".
    )
