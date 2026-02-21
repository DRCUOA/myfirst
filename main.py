import sys

from dotenv import load_dotenv

from .graph import app
from .state import State

load_dotenv()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m myfirst \"your prompt\"")
        sys.exit(2)
    user_input = sys.argv[1]
    state: State = {"input": user_input, "messages": [], "done": False}
    out = app.invoke(state)
    print("\n--- OUTPUT ---")
    for i, msg in enumerate(out["messages"], 1):
        print(f"{i}. {msg}")


if __name__ == "__main__":
    main()
