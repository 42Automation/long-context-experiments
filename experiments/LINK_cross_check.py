EXPERIMENTS = [
    {
        "id": "link_cross_check_two_segments",
        "query": "Are there any discrepancies in the revenue and gross profit values between prospectus and annual report?",
        "reference_doc_urls": [
            "./txt/LINK_gross_profit_prospectus.txt",
            "./txt/LINK_gross_profit_annual_report.txt",
        ],
        "expected_answer": "Yes, there are discrepancies. In particular, the revenue per segment for Central Europe in 2019 is 596,805K NOK in the annual report and 639,486K NOK in the prospectus, which also causes the totals to differ with 2,890,025K NOK in the annual report and 2,932,707K NOK in the prospectus.",
    },
    {
        "id": "link_cross_check_report_and_segment",
        "query": "Are there any discrepancies in the revenue and gross profit values between prospectus and annual report?",
        "reference_doc_urls": [
            "./txt/LINK_prospectus_main.txt",
            "./txt/LINK_gross_profit_annual_report.txt",
        ],
        "expected_answer": "Yes, there are discrepancies. In particular, the revenue per segment for Central Europe in 2019 is 596,805K NOK in the annual report and 639,486K NOK in the prospectus, which also causes the totals to differ with 2,890,025K NOK in the annual report and 2,932,707K NOK in the prospectus.",
    },
    {
        "id": "link_cross_check_two_reports",
        "query": "Are there any discrepancies in the revenue and gross profit values between prospectus and annual report?",
        "reference_doc_urls": [
            "./txt/LINK_prospectus_main.txt",
            "./txt/LINK Annual Report 2020 extract.txt",
        ],
        "expected_answer": "Yes, there are discrepancies. In particular, the revenue per segment for Central Europe in 2019 is 596,805K NOK in the annual report and 639,486K NOK in the prospectus, which also causes the totals to differ with 2,890,025K NOK in the annual report and 2,932,707K NOK in the prospectus.",
    },
]
