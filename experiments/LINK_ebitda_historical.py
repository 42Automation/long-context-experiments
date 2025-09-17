EXPERIMENTS = [
    {
        "id": "link_ebitda_historical_two_segments",
        "query": "Check the historical adjusted EBITDA values between the IPO prospectus and the Annual report. Do they match?",
        "reference_doc_urls": [
            "./txt/LINK_ebitda_historical_prospectus.txt",
            "./txt/LINK_ebitda_historical_annual_report.txt",
        ],
        "expected_answer": "The data in the documents provided allows us to compare historical adjusted EBITDA data for 2019 (previous years are not documented in the yearly report and 2020 is partially forecasted in the prospectus). For 2019, there are slight variations in adjusted EBITDA values reported. It can be found reported as 307,941 NOKK, or as 307,549 NOKK or as 307.5 NOKM or as 307,548 NOKK. So the values don't fully match, though they are all within 307.5 and 307.9 NOKM.",
    },
    {
        "id": "link_ebitda_historical_report_and_segment",
        "query": "Check the historical adjusted EBITDA values between the IPO prospectus and the Annual report. Do they match?",
        "reference_doc_urls": [
            "./txt/LINK_prospectus_main.txt",
            "./txt/LINK_ebitda_historical_annual_report.txt",
        ],
        "expected_answer": "The data in the documents provided allows us to compare historical adjusted EBITDA data for 2019 (previous years are not documented in the yearly report and 2020 is partially forecasted in the prospectus). For 2019, there are slight variations in adjusted EBITDA values reported. It can be found reported as 307,941 NOKK, or as 307,549 NOKK or as 307.5 NOKM or as 307,548 NOKK. So the values don't fully match, though they are all within 307.5 and 307.9 NOKM.",
    },
    {
        "id": "link_ebitda_historical_two_reports",
        "query": "Check the historical adjusted EBITDA values between the IPO prospectus and the Annual report. Do they match?",
        "reference_doc_urls": [
            "./txt/LINK_prospectus_main.txt",
            "./txt/LINK Annual Report 2020 extract.txt",
        ],
        "expected_answer": "The data in the documents provided allows us to compare historical adjusted EBITDA data for 2019 (previous years are not documented in the yearly report and 2020 is partially forecasted in the prospectus). For 2019, there are slight variations in adjusted EBITDA values reported. It can be found reported as 307,941 NOKK, or as 307,549 NOKK or as 307.5 NOKM or as 307,548 NOKK. So the values don't fully match, though they are all within 307.5 and 307.9 NOKM.",
    },
]
