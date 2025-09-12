EXPERIMENTS = [
    {
        "id": "link_q1_segment",
        "query": "What was LINK Mobility revenue in 2020?",
        "reference_doc_urls": [
            "./txt/LINK_revenue.txt",
        ],
        "expected_answer": "NOK 3 539 million",
    },
    {
        "id": "link_q1_one_report",
        "query": "What was LINK Mobility revenue in 2020?",
        "reference_doc_urls": ["./txt/LINK Annual Report 2020.txt"],
        "expected_answer": "NOK 3 539 million",
    },
    {
        "id": "link_q1_two_reports",
        "query": "What was LINK Mobility revenue in 2020?",
        "reference_doc_urls": ["./txt/LINK Annual Report 2020.txt"],
        "filler_doc_urls": ["./txt/LINK Annual Report 2021.txt"],
        "expected_answer": "NOK 3 539 million",
    },
]
