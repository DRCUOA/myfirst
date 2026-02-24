from langgraph.graph import StateGraph, START, END

from .state import State
from .nodes import echo_node, llm_node


def build_app(checkpointer=None):
    """Build and compile the graph. Pass a checkpointer for state persistence."""
    g = StateGraph(State)
    g.add_node("echo", echo_node)
    g.add_node("llm", llm_node)
    g.add_edge(START, "echo")
    g.add_edge("echo", "llm")
    g.add_edge("llm", END)
    return g.compile(checkpointer=checkpointer)