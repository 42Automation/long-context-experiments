EXPERIMENTS = [
    # SEGMENT
    {
        "id": "segment_pdf_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "reference_doc_urls": [
            "./pdf/Apple_segment_operating_performance.pdf",
        ],
        "expected_answer": "$25,052 million",
    },
    # SEC 24
    {
        "id": "sec24_pdf_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "reference_doc_urls": [
            "./pdf/Apple_SEC_filing_2024.pdf",
        ],
        "expected_answer": "$25,052 million",
    },
    # All SEC
    {
        "id": "all_sec_pdf_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "reference_doc_urls": [
            "./pdf/Apple_SEC_filing_2024.pdf",
            "./pdf/Apple_SEC_filing_2023.pdf",
            "./pdf/Apple_SEC_filing_2022.pdf",
        ],
        "expected_answer": "$25,052 million",
    },
]
