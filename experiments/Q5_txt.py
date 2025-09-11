EXPERIMENTS = [
    {
        "id": "q4_two_segments",
        "query": "Who had more FTEs in 2024, Apple or Tesla?",
        "reference_doc_urls": [
            "./txt/Apple_employees.txt",
            "./txt/Tesla_employees.txt",
        ],
        "expected_answer": "Apple",
    },
    {
        "id": "q4_two_sec",
        "query": "Who had more FTEs in 2024, Apple or Tesla?",
        "reference_doc_urls": ["./txt/Apple_SEC_filing_2024.txt"],
        "filler_doc_urls": ["./txt/Tesla_SEC_filing_2024.txt"],
        "expected_answer": "Apple",
    },
]
