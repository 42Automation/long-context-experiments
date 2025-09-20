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

DOC_TEMPLATE = """Here are some excerpts from the following document for your consideration:
<{filename}>
{content}
</{filename}>
"""

EXCERPT_TEMPLATE = """<excerpt_{index}>
{content}
</excerpt_{index}>
"""

JUDGE_SYSTEM_PROMPT = (
    "You are a helpful assistant. Provide accurate judgement for the queries provided"
)

QUERY_SYSTEM_PROMPT = """You are a helpful assistant. Answer the user query succintly.
If documents are provided, use them for answering the query.
When comparing values, focus on values which can be compared. Do not compare values which belong to different periods or regions, for instance.
"""


RETRIEVAL_AGENT_DESCRIPTION_TEMPLATE = """A team member that will retrieve information from the reference documents,
which is relevant to the user query.
You can retrieve with varying depth, as indicated by the k parameter.
Your max value for k is {k_max}.
"""

MANAGER_AGENT_PROMPT_TEMPLATE = """You are an expert financial advisor and need to answer a user query.

In order to answer the query, you need to consider information from one or more reference documents, which have already been provided to you.
You can ask your retriever agent for such information, as needed.

ATTENTION: The provided document are loaded with complex financial information.
Use all your expertise to devise a good strategy to answer the query.

HINT: You may need to break down the user query in different retrieval tasks,
to make sure you collect all needed information before providing your final answer.

Here is the user query:
<user_query>
{user_query}
</user_query>

Now, work hard to answer the user query fully and accurately. Use multiple steps if needed.
"""
