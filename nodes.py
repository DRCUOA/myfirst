import os
from openai import OpenAI

from .state import State

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    return _client


def echo_node(state: State) -> State:
    text = state["input"].strip()
    state["messages"].append(f"echo: {text}")
    state["done"] = True
    return state


def llm_node(state: State) -> State:
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
    state["messages"].append(answer.strip())
    state["done"] = True
    return state