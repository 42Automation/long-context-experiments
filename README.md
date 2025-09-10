# Experiments for long context on various LLMs

We explore the performance of frontier LLMs when retrieving information over financial documents over increasingly long contexts.

## Documents

We consider 2 set of documents:
* Apple SEC filings between 2022 and 2024
* Tesla SEC filings between 2022 and 2024

## Query types

We consider the following kinds of queries in our analysis, of increasing difficulty:
* Q1. Direct query. The information is found directly in the document, so a direct retrieval by lexical match is possible.
* Q2. Derived query. The information is found in the document, but it needs a reasoning step to relate it to the question.
* Q3. Distant info query. The information is found in the document, but the answer needs to combine distant pieces of information from the same document.
* Q4. Distractor loaded query. The information is found in the document, but the document has similar, yet conflicting pieces of information.

---
* Q4. Multiple document query. The needed information is found in the documents but the answer needs to combine information over multiple documents.
* Q5. Missing data query. The information requested is not found in the document, though it is semantically related to the document content, so the query cannot be answered.
* Q6. Ambiguous query. The exact information requested is not directly found in the document but a very close piece of information is available.
* Q7. Very ambiguous query. The exact information requested is not found in the document and it takes some reasoning to relate available content to the question.

## Actual queries

For the Apple SEC filings:
* Q1. What is the net sales for Japan in 2024?
* Q2. What year had the biggest operating expenditure for Apple?
* Q3. What is the net income per FTE in 2024 at Apple?
* Q4. What determines the vesting conditions for performance awards in Apple's 2022 Stock Plan?


## References
* [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot#yarn)