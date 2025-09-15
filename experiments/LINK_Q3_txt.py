EXPERIMENTS = [
    {
        "id": "link_q3_segment",
        "query": "How could the M&A activity affect the PFIC status?",
        "reference_doc_urls": [
            "./txt/LINK_PFIC_test.txt",
        ],
        "expected_answer": "M&A can change the PFIC tests by altering the company’s income mix (adding businesses that generate more passive revenue or temporary transaction-related passive gains) and by changing the asset composition (bringing in cash, receivables, or marketable investments or creating goodwill/intangibles) so that passive income or passive assets exceed the PFIC thresholds.",
    },
    {
        "id": "link_q3_one_report",
        "query": "How could the M&A activity affect the PFIC status?",
        "reference_doc_urls": ["./txt/LINK_prospectus_main.txt"],
        "expected_answer": "M&A can change the PFIC tests by altering the company’s income mix (adding businesses that generate more passive revenue or temporary transaction-related passive gains) and by changing the asset composition (bringing in cash, receivables, or marketable investments or creating goodwill/intangibles) so that passive income or passive assets exceed the PFIC thresholds.",
    },
    {
        "id": "link_q3_two_reports",
        "query": "How could the M&A activity affect the PFIC status?",
        "reference_doc_urls": ["./txt/LINK_prospectus_main.txt"],
        "filler_doc_urls": ["./txt/LINK Annual Report 2021.txt"],
        "expected_answer": "M&A can change the PFIC tests by altering the company’s income mix (adding businesses that generate more passive revenue or temporary transaction-related passive gains) and by changing the asset composition (bringing in cash, receivables, or marketable investments or creating goodwill/intangibles) so that passive income or passive assets exceed the PFIC thresholds.",
    },
]
