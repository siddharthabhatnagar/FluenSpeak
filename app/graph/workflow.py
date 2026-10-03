from typing import Dict, Any
from .state import FluenSpeakState
from .nodes import analyze_and_continue_node

try:
    from langgraph.graph import StateGraph, START, END
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False

class FallbackLangGraphWorkflow:
    """Seamless executor when running without langgraph package installed locally."""
    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await analyze_and_continue_node(state)

def create_fluenspeak_graph():
    """Builds and compiles the LangGraph StateGraph workflow for FluenSpeak dual-mode processing."""
    if HAS_LANGGRAPH:
        builder = StateGraph(FluenSpeakState)
        builder.add_node("analyze_and_continue", analyze_and_continue_node)
        builder.add_edge(START, "analyze_and_continue")
        builder.add_edge("analyze_and_continue", END)
        return builder.compile()
    else:
        return FallbackLangGraphWorkflow()

fluenspeak_graph = create_fluenspeak_graph()
