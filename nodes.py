import os
from openai import OpenAI

from .state import State

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    return _client


def echo_node(state: State) -> dict:
    text = state["input"].strip()
    return {"messages": [f"echo: {text}"], "done": True}


def llm_node(state: State) -> dict:
    """Calls OpenAI chat completions and appends the response to messages."""
    prompt = state["input"].strip()
    client = _get_client()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a concise helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    answer = resp.choices[0].message.content or ""
    return {"messages": [answer.strip()], "done": True}