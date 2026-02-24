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
    return {"messages": [{"role": "user", "content": text}], "done": True}


def _to_api_messages(messages: list) -> list[dict]:
    """Convert state messages to OpenAI API format. Handles both new (dict) and legacy (str) formats."""
    out = []
    for m in messages:
        if isinstance(m, dict) and "role" in m and "content" in m:
            out.append({"role": m["role"], "content": m["content"]})
        elif isinstance(m, str):
            # Legacy format: "echo: {user_input}" = user, anything else = assistant
            if m.startswith("echo: "):
                out.append({"role": "user", "content": m[6:].strip()})
            elif m.strip():
                out.append({"role": "assistant", "content": m.strip()})
    return out


DEFAULT_MODEL = "gpt-4o-mini"


def llm_node(state: State) -> dict:
    """Calls OpenAI chat completions with full conversation history."""
    client = _get_client()
    model = state.get("model") or DEFAULT_MODEL
    history = _to_api_messages(state["messages"])
    api_messages = [
        {"role": "system", "content": "You are a concise helpful assistant."},
        *history,
    ]
    resp = client.chat.completions.create(
        model=model,
        messages=api_messages,
    )
    answer = resp.choices[0].message.content or ""
    return {"messages": [{"role": "assistant", "content": answer.strip()}], "done": True}