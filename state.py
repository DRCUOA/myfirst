from typing import TypedDict, List

class State(TypedDict):
  input: str
  messages: List[str]
  done: bool


