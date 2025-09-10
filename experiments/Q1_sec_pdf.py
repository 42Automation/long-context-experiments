EXPERIMENTS = [
    # Two SEC docs
    {
        "id": "two_sec_txt_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "reference_docs_urls": [
            "./pdf/Apple_SEC_filing_2024.pdf",
            "./pdf/Apple_SEC_filing_2023.pdf",
        ],
        "expected_answer": "$25,052 million",
    },
]
