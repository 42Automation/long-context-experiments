# Inspired by https://github.com/chroma-core/context-rot/blob/master/experiments/niah_extension/evaluate/evaluate_niah_extension.py
JUDGE_PROMPT_TEMPLATE = """
Given this question and the CORRECT answer, determine whether the response is correct (meaning it factually aligns with the correct answer).
You must only respond with "true" or "false".
If the response is partially incorrect, such as a typo, respond with "false".
If the response contains a snippet of text or additional supporting information, while still maintaining the correct answer without changing the meaning, respond with "true".

Question:
<question>
{question}
</question>

CORRECT answer:
<correct_answer>
{correct_answer}
</correct_answer>

Response to judge:
<response_to_judge>
{output}
</response_tojudge>

Instructions: Respond with only "true" if the response factually aligns with the correct answer, or "false" if it does not. Do not provide any explanation - just "true" or "false".
"""

SYSTEM_PROMPT = """"You are a helpful assistant. Answer the user query succintly.
If documents are provided, use them for answering the query.
"""
