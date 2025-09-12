EXPERIMENTS = [
    {
        "id": "q6_segment",
        "query": "What were the costs of internal software tools development and maintenance for Apple in 2024?",
        "reference_doc_urls": [
            "./txt/Apple_internal_sw_dev.txt",
        ],
        "expected_answer": "The requested information could not be found in the provided documents.",
    },
    {
        "id": "q6_one_sec",
        "query": "What were the costs of internal software tools development and maintenance for Apple in 2024?",
        "reference_doc_urls": [
            "./txt/Apple_SEC_filing_2024.txt",
        ],
        "expected_answer": "The requested information could not be found in the provided documents.",
    },
    {
        "id": "q6_two_sec",
        "query": "What were the costs of internal software tools development and maintenance for Apple in 2024?",
        "reference_doc_urls": ["./txt/Apple_SEC_filing_2024.txt"],
        "filler_doc_urls": ["./txt/Tesla_SEC_filing_2024.txt"],
        "expected_answer": "The requested information could not be found in the provided documents.",
    },
]
