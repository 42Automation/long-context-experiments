EXPERIMENTS = [
    # SEGMENT
    {
        "id": "segment_txt_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "reference_docs_urls": [
            "./txt/Apple_segment_operating_performance.txt",
        ],
        "expected_answer": "$25,052 million",
    },
    # SEC 24
    {
        "id": "sec24_txt_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "reference_docs_urls": [
            "./txt/Apple_SEC_filing_2024.txt",
        ],
        "expected_answer": "$25,052 million",
    },
    # Two SEC docs
    {
        "id": "two_sec_txt_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "reference_docs_urls": ["./txt/Apple_SEC_filing_2024.txt"],
        "filler_docs_urls": ["./txt/Apple_SEC_filing_2023.txt"],
        "expected_answer": "$25,052 million",
    },
]
