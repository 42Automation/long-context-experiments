EXPERIMENTS = [
    {
        "id": "link_q2_segment",
        "query": "What currency pair has the strongest impact in case of exchange rates fluctuations?",
        "reference_doc_urls": [
            "./txt/LINK_exchange_rate.txt",
        ],
        "expected_answer": "NOK/EUR has the stronges impact in case of exchange rates fluctuations",
    },
    {
        "id": "link_q2_one_report",
        "query": "What currency pair has the strongest impact in case of exchange rates fluctuations?",
        "reference_doc_urls": ["./txt/LINK_prospectus_main.txt"],
        "expected_answer": "NOK/EUR has the stronges impact in case of exchange rates fluctuations",
    },
    {
        "id": "link_q2_two_reports",
        "query": "What currency pair has the strongest impact in case of exchange rates fluctuations?",
        "reference_doc_urls": ["./txt/LINK_prospectus_main.txt"],
        "filler_doc_urls": ["./txt/LINK Annual Report 2021.txt"],
        "expected_answer": "NOK/EUR has the stronges impact in case of exchange rates fluctuations",
    },
]
