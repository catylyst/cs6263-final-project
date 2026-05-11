# User Stories

> Every story below has a stable ID, a Given/When/Then statement, and numbered
> manual steps the TA can follow against the live `docker compose up` system.
> The TA scores Application Functionality by walking these stories against the
> live UI during Phase 3 of grading.
>
> Format conventions:
> - Story IDs are US-NN such as US-01, US-02, and US-03.
> - Filenames lowercase the prefix and use underscores.
> - US-01 maps to `test_us_01_no_retrieval.py` and `us_01_expected.png`.
> - Every story has a corresponding test in `tests/user_stories/`.
> - Every story has a reference screenshot in `docs/assets/stories/`.
> - Stories that exercise error paths are marked with `[ERROR PATH]`.
> - At least two stories must be error path stories.

---

## US-01: Answer a straightforward question with no retrieval

**As a** user  
**I want** a straightforward question to be answered without retrieval  
**So that** simple questions do not create unnecessary retrieval overhead.

**Acceptance criteria, Given / When / Then:**

> Given the application is running and the local corpus is available,  
> When the user submits the query "What is Adaptive RAG?",  
> Then the system classifies the query as label `A`, selects the `no_retrieval` strategy, returns a non-empty answer, uses `0` retrieval steps, and includes a request ID.

**Manual walkthrough steps:**

1. Confirm the app is running by visiting `http://localhost:8080`.
2. Confirm the home page shows a question input box and a `Submit` button.
3. Type `What is Adaptive RAG?` into the question input box.
4. Click `Submit`.
5. Observe the response area below the input box.
6. Verify that the response contains a non-empty answer.
7. Verify that the complexity label shown is `A`.
8. Verify that the selected strategy shown is `no_retrieval`.
9. Verify that retrieval steps equals `0`.
10. Verify that a request ID is displayed.
11. Compare the screen to `docs/assets/stories/us_01_expected.png`.

**Expected end state:**  
The UI displays an answer explaining Adaptive RAG, label `A`, strategy `no_retrieval`, retrieval steps `0`, and a visible request ID.

**Expected screenshot:**  
`docs/assets/stories/us_01_expected.png`

**Matching automated test:**  
`tests/user_stories/test_us_01_no_retrieval.py`

---

## US-02: Answer a single-hop question with one retrieval step

**As a** user  
**I want** a moderate question to use one retrieval step  
**So that** the system can answer with evidence from the local corpus without using unnecessary multi-step retrieval.

**Acceptance criteria, Given / When / Then:**

> Given the application is running and the local corpus is available,  
> When the user submits the query "What are the three routing labels in Adaptive RAG?",  
> Then the system classifies the query as label `B`, selects the `single_step` strategy, returns a non-empty answer, includes at least one citation, uses `1` retrieval step, and includes a request ID.

**Manual walkthrough steps:**

1. Confirm the app is running by visiting `http://localhost:8080`.
2. Confirm the home page shows a question input box and a `Submit` button.
3. Type `What are the three routing labels in Adaptive RAG?` into the question input box.
4. Click `Submit`.
5. Observe the response area below the input box.
6. Verify that the response contains a non-empty answer.
7. Verify that the answer mentions labels `A`, `B`, and `C`.
8. Verify that the complexity label shown is `B`.
9. Verify that the selected strategy shown is `single_step`.
10. Verify that retrieval steps equals `1`.
11. Verify that the citations section contains at least one citation.
12. Verify that each citation includes a document ID, title, snippet, and score.
13. Verify that a request ID is displayed.
14. Compare the screen to `docs/assets/stories/us_02_expected.png`.

**Expected end state:**  
The UI displays an answer describing the three Adaptive RAG routing labels, label `B`, strategy `single_step`, retrieval steps `1`, at least one citation, and a visible request ID.

**Expected screenshot:**  
`docs/assets/stories/us_02_expected.png`

**Matching automated test:**  
`tests/user_stories/test_us_02_single_step.py`

---

## US-03: Answer a complex question with multi-step retrieval

**As a** user  
**I want** a complex question to use multi-step retrieval  
**So that** the system can collect and combine evidence from more than one retrieval pass.

**Acceptance criteria, Given / When / Then:**

> Given the application is running and the local corpus is available,  
> When the user submits the query "How does Adaptive RAG balance accuracy and efficiency compared to always using multi-step retrieval?",  
> Then the system classifies the query as label `C`, selects the `multi_step` strategy, returns a non-empty answer, includes citations, uses `2` retrieval steps, and includes a request ID.

**Manual walkthrough steps:**

1. Confirm the app is running by visiting `http://localhost:8080`.
2. Confirm the home page shows a question input box and a `Submit` button.
3. Type `How does Adaptive RAG balance accuracy and efficiency compared to always using multi-step retrieval?` into the question input box.
4. Click `Submit`.
5. Observe the response area below the input box.
6. Verify that the response contains a non-empty answer.
7. Verify that the answer discusses both accuracy and efficiency.
8. Verify that the complexity label shown is `C`.
9. Verify that the selected strategy shown is `multi_step`.
10. Verify that retrieval steps equals `2`.
11. Verify that the citations section contains at least one citation.
12. Verify that a request ID is displayed.
13. Compare the screen to `docs/assets/stories/us_03_expected.png`.

**Expected end state:**  
The UI displays an answer explaining how Adaptive RAG balances accuracy and efficiency, label `C`, strategy `multi_step`, retrieval steps `2`, citations, and a visible request ID.

**Expected screenshot:**  
`docs/assets/stories/us_03_expected.png`

**Matching automated test:**  
`tests/user_stories/test_us_03_multi_step.py`

---

## US-04: Show evidence, routing decision, latency, and request ID

**As a** evaluator  
**I want** every successful response to show routing metadata and evidence  
**So that** I can verify how the system reached its answer during manual grading.

**Acceptance criteria, Given / When / Then:**

> Given the application is running and a valid question is submitted,  
> When the system returns a successful response,  
> Then the UI displays the final answer, complexity label, selected strategy, citations when used, retrieval step count, latency in milliseconds, and request ID.

**Manual walkthrough steps:**

1. Confirm the app is running by visiting `http://localhost:8080`.
2. Type `What are the three routing labels in Adaptive RAG?` into the question input box.
3. Click `Submit`.
4. Observe the response area below the input box.
5. Verify that the final answer is visible.
6. Verify that the complexity label is visible.
7. Verify that the selected strategy is visible.
8. Verify that retrieval step count is visible.
9. Verify that latency is visible in milliseconds.
10. Verify that request ID is visible.
11. Verify that at least one citation is visible for this single-step retrieval example.
12. Verify that the citation includes document ID, title, snippet, and score.
13. Compare the screen to `docs/assets/stories/us_04_expected.png`.

**Expected end state:**  
The UI displays the answer, routing decision, citations, retrieval steps, latency, and request ID in a readable format.

**Expected screenshot:**  
`docs/assets/stories/us_04_expected.png`

**Matching automated test:**  
`tests/user_stories/test_us_04_response_metadata.py`

---

## US-05 [ERROR PATH]: Empty input shows a clear error message

**As a** user  
**I want** clear feedback when I submit an empty question  
**So that** I know what to fix before trying again.

**Acceptance criteria, Given / When / Then:**

> Given the application is running,  
> When the user clicks `Submit` without entering any text,  
> Then the UI shows a clear error message and the API returns the error `input text is required`.

**Manual walkthrough steps:**

1. Confirm the app is running by visiting `http://localhost:8080`.
2. Leave the question input box empty.
3. Click `Submit`.
4. Observe the error message displayed near the input or response area.
5. Verify that the error message says `input text is required` or `Please enter a question`.
6. Verify that no Python stack trace appears in the UI.
7. Verify that no blank answer is shown.
8. Open browser developer tools and check the Network tab if available.
9. If an API request is sent, verify that the response status is `400`.
10. Verify that the API response body contains `input text is required`.
11. Compare the screen to `docs/assets/stories/us_05_expected.png`.

**Expected end state:**  
The UI displays a clear empty-input error message and does not show a blank answer or stack trace.

**Expected screenshot:**  
`docs/assets/stories/us_05_expected.png`

**Matching automated test:**  
`tests/user_stories/test_us_05_empty_input.py`

---

## US-06 [ERROR PATH]: No evidence returns a safe fallback

**As a** user  
**I want** the system to respond safely when no relevant evidence is found  
**So that** it does not hallucinate unsupported answers or crash.

**Acceptance criteria, Given / When / Then:**

> Given the application is running and the local corpus is available,  
> When the user submits a question that is unrelated to the corpus,  
> Then the system returns a safe fallback response, includes an empty citations list, does not crash, and includes a request ID.

**Manual walkthrough steps:**

1. Confirm the app is running by visiting `http://localhost:8080`.
2. Type `What is the maintenance schedule for the Mars colony water pump?` into the question input box.
3. Click `Submit`.
4. Observe the response area below the input box.
5. Verify that the system does not crash.
6. Verify that no Python stack trace appears in the UI.
7. Verify that the answer says `I could not find enough evidence in the local corpus to answer the question.` or an equivalent safe fallback message.
8. Verify that the citations section is empty or clearly states that no citations were found.
9. Verify that a request ID is displayed.
10. Compare the screen to `docs/assets/stories/us_06_expected.png`.

**Expected end state:**  
The UI displays a safe fallback answer, no citations, no stack trace, and a visible request ID.

**Expected screenshot:**  
`docs/assets/stories/us_06_expected.png`

**Matching automated test:**  
`tests/user_stories/test_us_06_no_evidence.py`

---

# Story to Test Mapping

| Story ID | Story title | Test file | Screenshot |
|---|---|---|---|
| US-01 | Answer a straightforward question with no retrieval | `tests/user_stories/test_us_01_no_retrieval.py` | `docs/assets/stories/us_01_expected.png` |
| US-02 | Answer a single-hop question with one retrieval step | `tests/user_stories/test_us_02_single_step.py` | `docs/assets/stories/us_02_expected.png` |
| US-03 | Answer a complex question with multi-step retrieval | `tests/user_stories/test_us_03_multi_step.py` | `docs/assets/stories/us_03_expected.png` |
| US-04 | Show evidence, routing decision, latency, and request ID | `tests/user_stories/test_us_04_response_metadata.py` | `docs/assets/stories/us_04_expected.png` |
| US-05 | Empty input shows a clear error message | `tests/user_stories/test_us_05_empty_input.py` | `docs/assets/stories/us_05_expected.png` |
| US-06 | No evidence returns a safe fallback | `tests/user_stories/test_us_06_no_evidence.py` | `docs/assets/stories/us_06_expected.png` |

# Notes for Manual Grading

The TA should be able to complete all six stories using only the running application and this document.

The application must be reachable from:

```text
http://localhost:8080
```

The API endpoint used by automated tests is:

```text
POST /api/query
```

Each successful API response must contain:

```text
request_id
question
complexity_label
strategy
answer
citations
retrieval_steps
latency_ms
```

The two required error-path stories are:

```text
US-05 [ERROR PATH]: Empty input shows a clear error message
US-06 [ERROR PATH]: No evidence returns a safe fallback
```
