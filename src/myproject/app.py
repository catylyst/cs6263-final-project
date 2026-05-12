"""Application entry point for the Adaptive RAG project.

This module provides a simple command-line demo entry point. The main grading
interface is the FastAPI app in src/myproject/api.py.
"""

from __future__ import (
    annotations,  # This import allows for the use of forward references in type annotations, enabling the use of types that are defined later in the code.
)

import json  # The json module is imported to allow for the conversion of Python objects to JSON format, which is useful for displaying the results of the demo in a readable format.

from myproject.router import (
    route_query,  # Importing the route_query function from the router module in the myproject package, which is used to process user queries and generate answers based on the defined strategies.
)


def run_demo() -> (
    None
):  # This function defines a simple command-line demo that runs a few example questions through the route_query function and prints the results in JSON format.
    """Run a small local demo from the command line."""
    questions = [
        "What is Adaptive RAG?",
        "What are the three routing labels in Adaptive RAG?",
        "How does Adaptive RAG balance accuracy and efficiency compared to always using multi-step retrieval?",
    ]

    for question in questions:
        result = route_query(question)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run_demo()
