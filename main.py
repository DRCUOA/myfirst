import argparse
import sys
import warnings

warnings.filterwarnings("ignore", message=".*Pydantic V1.*Python 3.14.*", category=UserWarning)

from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver

from .graph import build_app
from .prompt import build_prompt
from .state import State

load_dotenv()


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
        "-t", "--thread",
        metavar="ID",
        default="default",
        help="Thread ID for conversation context (default: default)",
    )
    parser.add_argument(
        "-s", "--simple",
        action="store_true",
        help="Print only the last (assistant) message, for chat UIs",
    )
    parser.add_argument(
        "prompt",
        help="Your prompt (required)",
    )
    args = parser.parse_args()

    files = None
    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                files = [{"name": args.file, "content": f.read()}]
        except OSError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    prompt = build_prompt(args.prompt, files)
    state: State = {"input": prompt, "messages": [], "done": False}
    config = {"configurable": {"thread_id": args.thread}}

    with SqliteSaver.from_conn_string("langgraph.db") as checkpointer:
        app = build_app(checkpointer=checkpointer)
        out = app.invoke(state, config)
    def _content(msg) -> str:
        return msg["content"] if isinstance(msg, dict) else str(msg)

    if args.simple:
        if out["messages"]:
            print(_content(out["messages"][-1]))
    else:
        print("\n--- OUTPUT ---")
        for i, msg in enumerate(out["messages"], 1):
            print(f"{i}. {_content(msg)}")


if __name__ == "__main__":
    main()
