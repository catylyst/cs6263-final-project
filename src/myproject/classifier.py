"""Query complexity for the Adaptive RAG project.

The classifier pedicts one of three labes:

A = no retrieval needed
B = single-step retrieval needed
C = multi-step retrieval needed

This project uses a determinsitic rule basd clasifier so the system
is reproducible and does not requre an external model API during grading.
"""

from __future__ import annotations # This import allows for the use of forward references in type annotations, enabling the use of types that are defined later in the code.

import re # The regular expression module is imported to perform pattern matching on the input question text.

def _normalize(text: str) -> str:
    """Normalize question text for simple rule making"""
    
    return " ".join(text.lower().strip().split()) # This function takes a string input, converts it to lowercase, removes leading and trailing whitespace, and collapses multiple spaces into a single space. This normalization helps ensure that the pattern matching is consistent regardless of the input formatting.

def _count_question_marks(text: str) -> int:
    """Count the number of question marks in the text."""

    return text.count("?") # This function counts the number of question marks in the input text, which can be an indicator of question complexity.

def _contains_any(text: str, phrases: list[str]) -> bool:
    """Return True when any phrase appears in the normalized text."""

    return any(phrase in text for phrase in phrases) # This function checks if any of the specified phrases are present in the input text, which can be used to identify certain types of questions that may require retrieval.

def classify_query(text: str) -> str:
    """Return query complexity label "A", "B", or "C",

    A means the question is straightforward and can be answered without retrieval.
    B means the question requires retrieval of relevant information to answer.  
    C means the question is complex and may require multiple retrieval steps or reasoning.
    
    Parameters:
    -----------
    text:
        User question text to classify.
    
    Returns
    --------
    str:
        Complexity label "A", "B", or "C".
    """

    normalized = _normalize(text) # The input text is normalized to ensure consistent pattern matching.

    if not normalized:
        raise ValueError("input text is required")# If the normalized text is empty, a ValueError is raised indicating that input text is required for classification.

    complex_phrases = [
        "compare",
        "compared to",
        "relationship between",
        "based on both",
        "how does",
        "why does",
        "what happened after",
        "who is the person that",
        "which document explains",
        "multi-step",
        "multi step",
        "chain",
        "chained",
        "evidence from multiple",
        "accuracy and efficiency",
        "balance accuracy and efficiency",
        "always using multi-step retrieval",
    ] # A list of phrases that are indicative of complex questions that may require multi-step retrieval or reasoning.

    single_step_phrases = [
        "three routing labels",
        "routing labels",
        "label a",
        "label b",
        "label c",
        "single-step",
        "single step",
        "one retrieval",
        "citation",
        "corpus",
        "retrieval strategy",
        "query complexity classifier",
    ] # A list of phrases that are indicative of questions that require single-step retrieval.

    simple_phrases = [
        "what is adaptive rag",
        "define adaptive rag",
        "what is adaptive-rag",
        "what does adaptive rag mean",
    ] # A list of phrases that are indicative of simple questions that can be answered without retrieval.

    if _contains_any(normalized, complex_phrases):
        return "C" # If any of the complex phrases are found in the normalized text, the function returns "C", indicating that the question is complex and may require multiple retrieval steps or reasoning.

    if _contains_any(normalized, single_step_phrases):
        return "B" # If any of the single-step phrases are found in the normalized text, the function returns "B", indicating that the question requires retrieval of relevant information to answer.

    if _contains_any(normalized, simple_phrases):
        return "A" # If any of the simple phrases are found in the normalized text, the function returns "A", indicating that the question is straightforward and can be answered without retrieval.

    word_count = len(re.findall(r"\b\w+\b", normalized)) # This line uses a regular expression to find all word tokens in the normalized text and counts them. The pattern \b\w+\b matches sequences of word characters that are bounded by word boundaries, effectively counting the number of words in the question.
    question_count = _count_question_marks(normalized) # This line counts the number of question marks in the normalized text, which can be an indicator of question complexity. A higher number of question marks may suggest that the question is more complex and may require more retrieval steps to answer.

    if word_count <= 5 and question_count <= 1:
        return "A" # If the word count is 5 or fewer and there is at most 1 question mark, the function returns "A", indicating that the question is likely straightforward and can be answered without retrieval.

    if word_count >= 14 or question_count > 1:
        return "C" # If the word count is 14 or more, or if there are more than 1 question marks, the function returns "C", indicating that the question is likely complex and may require multiple retrieval steps or reasoning.

    return "B" # If none of the above conditions are met, the function defaults to returning "B", indicating that the question likely requires retrieval of relevant information to answer, but is not complex enough to require multiple retrieval steps.