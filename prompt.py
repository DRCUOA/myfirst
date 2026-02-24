"""Build prompts with optional file context."""


def build_prompt(user_input: str, files: list[dict] | None = None) -> str:
    """Build a prompt with optional file contents embedded.

    Args:
        user_input: The user's message.
        files: Optional list of {name: str, content: str} to embed.

    Returns:
        The full prompt with file context if provided.
    """
    if not files:
        return user_input
    parts = []
    for f in files:
        name = f.get("name", "file")
        content = f.get("content", "")
        parts.append(f"--- Content from {name} ---\n\n{content}\n\n--- End of file ---")
    parts.append(user_input)
    return "\n\n".join(parts)
