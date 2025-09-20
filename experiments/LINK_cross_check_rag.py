EXPERIMENTS = [
    {
        "id": "link_cross_check_rag_k5",
        "query": "Are there any discrepancies in the revenue and gross profit values between prospectus and annual report?",
        "reference_doc_urls": [
            "./pdf/LINK_prospectus_main.pdf",
            "./pdf/LINK Annual Report 2020.pdf",
        ],
        "treatments": {"rag": {"k": 5}},
        "expected_answer": "Yes, there are discrepancies. In particular, the revenue per segment for Central Europe in 2019 is 596,805K NOK in the annual report and 639,486K NOK in the prospectus, which also causes the totals to differ with 2,890,025K NOK in the annual report and 2,932,707K NOK in the prospectus.",
    },
    {
        "id": "link_cross_check_rag_k10",
        "query": "Are there any discrepancies in the revenue and gross profit values between prospectus and annual report?",
        "reference_doc_urls": [
            "./pdf/LINK_prospectus_main.pdf",
            "./pdf/LINK Annual Report 2020.pdf",
        ],
        "treatments": {"rag": {"k": 10}},
        "expected_answer": "Yes, there are discrepancies. In particular, the revenue per segment for Central Europe in 2019 is 596,805K NOK in the annual report and 639,486K NOK in the prospectus, which also causes the totals to differ with 2,890,025K NOK in the annual report and 2,932,707K NOK in the prospectus.",
    },
]
