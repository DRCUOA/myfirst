from typing import TypedDict, List, Annotated
import operator

class State(TypedDict):
    input: str
    # reducer: when multiple updates occur, lists are combined via +
    messages: Annotated[List[str], operator.add]
    done: bool

