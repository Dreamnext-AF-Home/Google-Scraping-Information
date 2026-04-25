import os
from langchain_openai import ChatOpenAI
from datetime import datetime

# User agents for web scraping
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
]

_llm_cache: dict = {}

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

async def ainvoke_llm(
    model,
    system_prompt,
    user_message,
    response_format=None,
    temperature=0.1
):
    api_key = os.getenv("OPENROUTER_API_KEY")
    cache_key = (model, api_key, temperature)

    if cache_key not in _llm_cache:
        _llm_cache[cache_key] = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
        )

    llm = _llm_cache[cache_key]

    if response_format:
        llm = llm.with_structured_output(response_format)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    response = await llm.ainvoke(messages)

    return response if response_format else response.content
