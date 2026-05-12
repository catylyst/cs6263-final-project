"""Local corpus retriever for the Adaptive RAG project.

The retriever loads a JSONL corpus and performs lightweight TF-IDF search.
It returns citations with document ID, title, snippet, and similarity score.
"""

from __future__ import annotations  # Delays type-hint evaluation, which helps with cleaner modern type hints.

import json  # Imports Python's built-in JSON library so we can read JSONL records.
from pathlib import Path  # Imports Path, which makes file paths easier and safer to work with.

from sklearn.feature_extraction.text import TfidfVectorizer  # Converts text documents into TF-IDF numeric vectors.
from sklearn.metrics.pairwise import cosine_similarity  # Measures similarity between the query vector and document vectors.

from myproject.schemas import CorpusDocument  # Imports the Pydantic model used to validate corpus documents.


class Retriever:
    """Search a local JSONL document corpus using TF-IDF similarity."""

    def __init__(self, corpus_path: str) -> None:
        """Load the local corpus and build a TF-IDF matrix.

        Parameters
        ----------
        corpus_path:
            Path to the JSONL corpus file.
        """

        self.corpus_path = Path(corpus_path)  # Converts the input file path string into a Path object.

        self.documents = self._load_corpus(self.corpus_path)  # Loads and validates all documents from the JSONL corpus.

        if not self.documents:  # Checks whether the corpus file loaded zero valid documents.
            raise ValueError(f"No documents found in corpus: {corpus_path}")  # Stops execution if the corpus is empty.

        self.texts = [doc.text for doc in self.documents]  # Extracts only the text field from each corpus document.

        self.vectorizer = TfidfVectorizer(stop_words="english")  # Creates a TF-IDF vectorizer and removes common English stop words.

        self.matrix = self.vectorizer.fit_transform(self.texts)  # Learns the vocabulary and converts all corpus texts into vectors.

    def _load_corpus(self, corpus_path: Path) -> list[CorpusDocument]:
        """Load corpus documents from a JSONL file."""

        if not corpus_path.exists():  # Checks whether the JSONL corpus file exists.
            raise FileNotFoundError(f"Corpus file not found: {corpus_path}")  # Stops execution if the file path is invalid.

        documents: list[CorpusDocument] = []  # Creates an empty list to store validated corpus documents.

        with corpus_path.open("r", encoding="utf-8") as file:  # Opens the corpus file for reading using UTF-8 encoding.
            for line_number, line in enumerate(file, start=1):  # Loops through the file one line at a time and tracks line numbers.
                stripped = line.strip()  # Removes leading and trailing whitespace from the current line.

                if not stripped:  # Checks whether the line is blank.
                    continue  # Skips blank lines and moves to the next line.

                try:  # Starts a block for code that might fail while parsing JSON.
                    row = json.loads(stripped)  # Converts the JSON string from the current line into a Python dictionary.

                    documents.append(CorpusDocument(**row))  # Validates the dictionary using CorpusDocument and adds it to the list.

                except json.JSONDecodeError as exc:  # Catches invalid JSON formatting errors.
                    raise ValueError(  # Raises a clearer error message for the user or developer.
                        f"Invalid JSON on line {line_number} in {corpus_path}"
                    ) from exc  # Keeps the original JSON error attached for debugging.

        return documents  # Returns the list of validated corpus documents.

    def search(self, query: str, k: int = 5) -> list[dict]:
        """Return the top k relevant passages.

        Parameters
        ----------
        query:
            User question.
        k:
            Maximum number of results to return.

        Returns
        -------
        list[dict]
            Each result contains doc_id, title, snippet, and score.
        """

        cleaned_query = " ".join(query.strip().split())  # Cleans the query by removing extra spaces, tabs, and newlines.

        if not cleaned_query:  # Checks whether the cleaned query is empty.
            return []  # Returns no results for an empty query.

        query_vector = self.vectorizer.transform([cleaned_query])  # Converts the user query into a TF-IDF vector using the same vocabulary.

        similarities = cosine_similarity(query_vector, self.matrix).flatten()  # Compares the query vector to every document vector.

        ranked_indices = similarities.argsort()[::-1]  # Sorts document indexes from highest similarity score to lowest.

        results: list[dict] = []  # Creates an empty list to store the final search results.

        for index in ranked_indices[:k]:  # Loops through only the top k ranked document indexes.
            score = float(similarities[index])  # Gets the similarity score for the current document as a regular float.

            if score <= 0.0:  # Ignores documents with no meaningful similarity to the query.
                continue  # Skips this document and checks the next ranked result.

            doc = self.documents[index]  # Retrieves the original CorpusDocument that matches the ranked index.

            results.append(  # Adds a formatted citation-style result to the output list.
                {
                    "doc_id": doc.doc_id,  # Includes the unique document ID for traceability.
                    "title": doc.title,  # Includes the document title for readability.
                    "snippet": self._make_snippet(doc.text),  # Includes a shortened text snippet from the document.
                    "score": round(score, 4),  # Includes the similarity score rounded to four decimal places.
                }
            )

        return results  # Returns the ranked list of relevant documents.

    @staticmethod  # Marks this method as independent from class instance data.
    def _make_snippet(text: str, max_chars: int = 280) -> str:
        """Return a readable citation snippet."""

        clean_text = " ".join(text.strip().split())  # Cleans the document text by removing extra whitespace.

        if len(clean_text) <= max_chars:  # Checks whether the text is already short enough.
            return clean_text  # Returns the full cleaned text when it fits within the limit.

        return clean_text[: max_chars - 3].rstrip() + "..."  # Truncates long text and adds an ellipsis.