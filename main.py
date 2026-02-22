import argparse
import sys
import warnings

warnings.filterwarnings("ignore", message=".*Pydantic V1.*Python 3.14.*", category=UserWarning)

from dotenv import load_dotenv

from .graph import app
from .state import State

load_dotenv()


def _build_prompt(user_input: str, file_path: str | None) -> str:
    if file_path is None:
        return user_input
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    return f"""--- Content from {file_path} ---

{content}

--- End of file ---

{user_input}"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the myfirst LangGraph app with an optional file context."
    )
    parser.add_argument(
        "-f", "--file",
        metavar="PATH",
        help="Path to a file whose contents will be embedded in the prompt",
    )
    parser.add_argument(
        "prompt",
        help="Your prompt (required)",
    )
    args = parser.parse_args()

    prompt = _build_prompt(args.prompt, args.file)
    state: State = {"input": prompt, "messages": [], "done": False}
    out = app.invoke(state)
    print("\n--- OUTPUT ---")
    for i, msg in enumerate(out["messages"], 1):
        print(f"{i}. {msg}")


if __name__ == "__main__":
    main()
