from typing import TypedDict, List, Annotated
import operator

# Each message: {"role": "user" | "assistant", "content": str}
Message = dict[str, str]


class State(TypedDict):
    input: str
    # reducer: when multiple updates occur, lists are combined via +
    messages: Annotated[List[Message], operator.add]
    done: bool
    model: str  # OpenAI model id, e.g. gpt-4o-mini (optional at runtime)

