"""Shared request and response models (schemas) for the Adaptive RAG project..

this modeulse defines teh public  data structure used by the API, router, retrievers,
and answer strategy modules. The shapes match the doc/SPEC.md and docs/STORIES.md.
"""

from __future__ import annotations 

from typing import Literal

from pydantic import BaseModel, Field

ComplexityLabel =  Literal["A", "B", "C"]
StrategyName = Literal["no_retrieval", "single_step", "multi_step"]

class QueryRequest(BaseModel):
    """Incoming API request for a user question."""

    text: str = Field(
        ..., # The ellipsis indicates that this field is required and must be provided in the request.
        min_length=1, # The minimum length of the question text is 1 character, ensuring that empty questions are not accepted.
        description="The user's question or query." # A human-readable description of the field, which can be used in API documentation and for clarity when debugging.
    )
    max_results: int = Field(
        default=5, # The maximum number of retrieved documents to return.
        ge=1, # The Minimum value is 1, ensuring at least one result is returned.
        le=20, # The Maximum value is 20, to prevent excessive results
        description="The maximum number of retrieved documents to return (1-20)."
    )
class Citation(BaseModel):
    """A retrieved evidence passage returned with an answer"""

    doc_id: str # Unique identifier for the retrieved document, which can be used for tracing and debugging.
    title: str # A human-readable title for the document, which can be useful for debugging and analysis.
    score: float = Field(ge=0.0) # The relevance score of the retrieved passage, which can be useful for debugging and analysis.
    
class QueryResponse(BaseModel):
    """Successful response retuerned by the Adaptive RAG system."""

    request_id: str # A unique identifier for the request, useful for tracing and debugging.
    question: str # The original user question, echoed back in the response for clarity.
    complexity_label: ComplexityLabel # A label indicating the complexity of the question, which can be used for analysis and debugging.
    strategy: StrategyName # The name of the answer strategy used to generate the answer, which can be useful for analysis and debugging.
    answer: str # The generated answer to the user's question, which may be based on retrieved evidence and reasoning.
    citations: list[Citation] # A list of retrieved evidence passages that were used to generate the answer, which can be useful for transparency and debugging.
    retrieval_steps: int = Field(ge=0) # The number of retrieval steps taken to generate the answer, which can be useful for analysis and debugging.
    latency_ms: int = Field(ge=0) # The total latency of the request in milliseconds, which can be useful for performance monitoring and debugging.

class ErrorResponse(BaseModel):
    """Standard error response"""

    error: str # A human-readable error message describing what went wrong, which can be useful for debugging and user feedback.

class CorpusDocument(BaseModel):
    """A document in the corpus, used for testing and retrieval."""

    doc_id: str # Unique identifier for the document
    title: str # A human-readable title for the document
    text: str # The full text content of the document, which will be indexed and retrieved by the system.
    source: str # The source of the document, such as a URL or database name, which can be useful for debugging and analysis.
    