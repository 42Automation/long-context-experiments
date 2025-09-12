EXPERIMENTS = [
    {
        "id": "q7_segment",
        "query": "How long is the performance period for vesting RSUs in Apple's Stock Plan?",
        "reference_doc_urls": [
            "./txt/Apple_performance_period.txt",
        ],
        "expected_answer": "The document does not explicitly state the duration of the Performance Period for the vesting of RSUs.",
    },
    {
        "id": "q7_one_sec",
        "query": "How long is the performance period for vesting RSUs in Apple's Stock Plan?",
        "reference_doc_urls": [
            "./txt/Apple_SEC_filing_2024.txt",
        ],
        "expected_answer": "The document does not explicitly state the duration of the Performance Period for the vesting of RSUs.",
    },
    {
        "id": "q7_two_sec",
        "query": "How long is the performance period for vesting RSUs in Apple's Stock Plan?",
        "reference_doc_urls": ["./txt/Apple_SEC_filing_2024.txt"],
        "filler_doc_urls": ["./txt/Tesla_SEC_filing_2024.txt"],
        "expected_answer": "The document does not explicitly state the duration of the Performance Period for the vesting of RSUs.",
    },
]
