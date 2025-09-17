EXPERIMENTS = [
    {
        "id": "link_ebitda_forecast_two_segments",
        "query": "Does the forecasted EBITDA for 2020 match the actual values?",
        "reference_doc_urls": [
            "./txt/LINK_ebitda_prospectus.txt",
            "./txt/LINK_ebitda_annual_report.txt",
        ],
        "expected_answer": "No, the prospectus forescast for the 2020 EBITDA is NOK 360 million to NOK 370 million but the actual values is roughly 390 million, according to the annual report.",
    },
    {
        "id": "link_ebitda_forecast_report_and_segment",
        "query": "Does the forecasted EBITDA for 2020 match the actual values?",
        "reference_doc_urls": [
            "./txt/LINK_prospectus_main.txt",
            "./txt/LINK_ebitda_annual_report.txt",
        ],
        "expected_answer": "No, the prospectus forescast for the 2020 EBITDA is NOK 360 million to NOK 370 million but the actual values is roughly 390 million, according to the annual report.",
    },
    {
        "id": "link_ebitda_forecast_two_reports",
        "query": "Does the forecasted EBITDA for 2020 match the actual values?",
        "reference_doc_urls": [
            "./txt/LINK_prospectus_main.txt",
            "./txt/LINK Annual Report 2020 extract.txt",
        ],
        "expected_answer": "No, the prospectus forescast for the 2020 EBITDA is NOK 360 million to NOK 370 million but the actual values is roughly 390 million, according to the annual report.",
    },
]
