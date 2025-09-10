EXPERIMENTS = [
    {
        "id": "q4_segment",
        "query": "What determines the vesting conditions for performance awards in Apple's 2022 Stock Plan?",
        "reference_doc_urls": [
            "./txt/Apple_performance_award.txt",
        ],
        "expected_answer": "Vesting is contingent upon the achievement of specific company performance metrics. In this case, it's tied to Apple's relative Total Shareholder Return (TSR) percentile performance compared to a defined group of peer companies over a predetermined performance period.",
    },
    {
        "id": "q4_one_sec",
        "query": "What determines the vesting conditions for performance awards in Apple's 2022 Stock Plan?",
        "reference_doc_urls": [
            "./txt/Apple_SEC_filing_2024.txt",
        ],
        "expected_answer": "Vesting is contingent upon the achievement of specific company performance metrics. In this case, it's tied to Apple's relative Total Shareholder Return (TSR) percentile performance compared to a defined group of peer companies over a predetermined performance period.",
    },
    {
        "id": "q4_two_sec",
        "query": "What determines the vesting conditions for performance awards in Apple's 2022 Stock Plan?",
        "reference_doc_urls": ["./txt/Apple_SEC_filing_2024.txt"],
        "filler_doc_urls": ["./txt/Tesla_SEC_filing_2024.txt"],
        "expected_answer": "Vesting is contingent upon the achievement of specific company performance metrics. In this case, it's tied to Apple's relative Total Shareholder Return (TSR) percentile performance compared to a defined group of peer companies over a predetermined performance period.",
    },
]
