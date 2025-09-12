EXPERIMENTS = [
    {
        "id": "q3_segment",
        "query": "What is the net income per FTE in 2024 at Apple?",
        "reference_doc_urls": [
            "./txt/Apple_net_income.txt",
        ],
        "expected_answer": "93,736,000 / 164,000, which is over $570K per FTE",
    },
    {
        "id": "q3_one_sec",
        "query": "What is the net income per FTE in 2024 at Apple?",
        "reference_doc_urls": [
            "./txt/Apple_SEC_filing_2024.txt",
        ],
        "expected_answer": "93,736,000 / 164,000, which is over $570K per FTE",
    },
    {
        "id": "q3_two_sec",
        "query": "What is the net income per FTE in 2024 at Apple?",
        "reference_doc_urls": ["./txt/Apple_SEC_filing_2024.txt"],
        "filler_doc_urls": ["./txt/Tesla_SEC_filing_2024.txt"],
        "expected_answer": "93,736,000 / 164,000, which is over $570K per FTE",
    },
]
