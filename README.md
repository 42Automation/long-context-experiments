# Experiments for long context on various LLMs

We explore the performance of frontier LLMs when retrieving information over financial documents over increasingly long contexts.

## Documents

We consider 2 sets of documents:

SEC filings:
* Apple SEC filings between 2022 and 2024
* Tesla SEC filings between 2022 and 2024

Prospectus and annual reports from LINK Mobility:
* LINK Mobility IPO Prospectus 2020
* LINK Annual Report 2021
* LINK Annual Report 2020

## Query types

We consider the following kinds of queries in our analysis, of increasing difficulty:
* Q1. Direct query. The information is found directly in the document, so a direct retrieval by lexical match is possible.
* Q2. Derived query. The information is found in the document, but it needs a reasoning step to relate it to the question.
* Q3. Distant info query. The information is found in the document, but the answer needs to combine distant pieces of information from the same document.
* Q4. Distractor loaded query. The information is found in the document, but the document has similar, yet conflicting pieces of information.
* Q5. Multiple document query. The needed information is found in the documents but the answer needs to combine information over multiple documents.
* Q6. Missing data query. The information requested is not found in the document, though it is semantically related to the document content, so the query cannot be answered.
* Q7. Ambiguous query. The exact information requested is not directly found in the document but a very close piece of information is available.

## Actual queries

For the SEC filing documents:
* Q1. What is the net sales for Japan in 2024?
* Q2. What year had the biggest operating expenditure for Apple?
* Q3. What is the net income per FTE in 2024 at Apple?
* Q4. What determines the vesting conditions for performance awards in Apple's 2022 Stock Plan?
* Q5. Who has more FTEs in 2024, Apple or Tesla?
* Q6. What were the costs of internal software tools development and maintenance for Apple in 2024?
* Q7. How long is the performance period for vesting RSUs in Apple's Stock Plan?

For the LINK mobility documents:
* Q1. What was LINK Mobility revenue in 2020?


## References
* [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot#yarn)