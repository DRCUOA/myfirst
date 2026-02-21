from langgraph.graph import StateGraph, START, END
from .state import State
from .nodes import echo_node
def build_app():
 g = StateGraph(State)
 g.add_node("echo", echo_node)
 g.add_edge(START, "echo")
 g.add_edge("echo", END)
 return g.compile()
app = build_app()