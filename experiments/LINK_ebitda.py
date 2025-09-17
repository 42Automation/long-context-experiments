EXPERIMENTS = [
    {
        "id": "link_ebitda_two_segments",
        "query": "Check the full-year EBITDA values between the IPO prospectus and the Annual report. Do they match?",
        "reference_doc_urls": [
            "./txt/LINK_ebitda_prospectus.txt",
            "./txt/LINK_ebitda_annual_report.txt",
        ],
        "expected_answer": "Yes, from the values provided, the EBITDA values for 2019 are consistent.",
    },
    {
        "id": "link_cross_check_report_and_segment",
        "query": "Check the full-year EBITDA values between the IPO prospectus and the Annual report. Do they match?",
        "reference_doc_urls": [
            "./txt/LINK_prospectus_main.txt",
            "./txt/LINK_ebitda_annual_report.txt",
        ],
        "expected_answer": "Yes, from the values provided, the EBITDA values for 2019 are consistent.",
    },
    {
        "id": "link_cross_check_two_reports",
        "query": "Check the full-year EBITDA values between the IPO prospectus and the Annual report. Do they match?",
        "reference_doc_urls": [
            "./txt/LINK_prospectus_main.txt",
            "./txt/LINK Annual Report 2020 extract.txt",
        ],
        "expected_answer": "Yes, from the values provided, the EBITDA values for 2019 are consistent.",
    },
]
