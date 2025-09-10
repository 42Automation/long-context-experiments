EXPERIMENTS = [
    {
        "id": "q2_segment",
        "query": "What year had the biggest operating expenditure for Apple?",
        "reference_docs_urls": [
            "./txt/Apple_operating_expenses.txt",
        ],
        "expected_answer": "2024",
    },
    {
        "id": "q2_one_sec",
        "query": "What year had the biggest operating expenditure for Apple?",
        "reference_docs_urls": [
            "./txt/Apple_SEC_filing_2024.txt",
        ],
        "expected_answer": "2024",
    },
    {
        "id": "q2_two_sec",
        "query": "What year had the biggest operating expenditure for Apple?",
        "reference_docs_urls": ["./txt/Apple_SEC_filing_2024.txt"],
        "filler_docs_urls": ["./txt/Tesla_SEC_filing_2024.txt"],
        "expected_answer": "2024",
    },
]
