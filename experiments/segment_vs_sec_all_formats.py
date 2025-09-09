EXPERIMENTS = [
    # SEGMENT
    {
        "id": "segment_pdf_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "docs": [
            "./pdf/Apple_segment_operating_performance.pdf",
        ],
        "expected_answer": "$25,052 million",
    },
    {
        "id": "segment_md_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "docs": [
            "./md/Apple_segment_operating_performance.md",
        ],
        "expected_answer": "$25,052 million",
    },
    {
        "id": "segment_txt_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "docs": [
            "./txt/Apple_segment_operating_performance.txt",
        ],
        "expected_answer": "$25,052 million",
    },
    # SEC 24
    {
        "id": "sec24_pdf_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "docs": [
            "./pdf/Apple_SEC_filing_2024.pdf",
        ],
        "expected_answer": "$25,052 million",
    },
    {
        "id": "sec24_md_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "docs": [
            "./md/Apple_SEC_filing_2024.md",
        ],
        "expected_answer": "$25,052 million",
    },
    {
        "id": "sec24_txt_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "docs": [
            "./txt/Apple_SEC_filing_2024.txt",
        ],
        "expected_answer": "$25,052 million",
    },
    # All SEC
    {
        "id": "all_sec_pdf_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "docs": [
            "./pdf/Apple_SEC_filing_2024.pdf",
            "./pdf/Apple_SEC_filing_2023.pdf",
            "./pdf/Apple_SEC_filing_2022.pdf",
        ],
        "expected_answer": "$25,052 million",
    },
    {
        "id": "all_sec_md_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "docs": [
            "./md/Apple_SEC_filing_2024.md",
            "./md/Apple_SEC_filing_2023.md",
            "./md/Apple_SEC_filing_2022.md",
        ],
        "expected_answer": "$25,052 million",
    },
    {
        "id": "all_sec_txt_net_sales_japan",
        "query": "What is the net sales for Japan in 2024?",
        "docs": [
            "./txt/Apple_SEC_filing_2024.txt",
            "./txt/Apple_SEC_filing_2023.txt",
            "./txt/Apple_SEC_filing_2022.txt",
        ],
        "expected_answer": "$25,052 million",
    },
]
