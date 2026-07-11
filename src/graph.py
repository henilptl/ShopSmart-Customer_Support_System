"""Assemble and compile the routing graph.

Shape:

    START -> classify_query -> (conditional) -> one of four handlers -> END
"""

from langgraph.graph import END, StateGraph

from .nodes import (
    classify_query,
    handle_billing,
    handle_order_status,
    handle_product_info,
    handle_returns,
    route_by_category,
)
from .state import AgentState

HANDLERS = [
    "handle_order_status",
    "handle_returns",
    "handle_billing",
    "handle_product_info",
]


def build_graph():
    """Build and compile the ShopSmart support router."""
    support_graph = StateGraph(AgentState)

    # 1. Register nodes
    support_graph.add_node("classify_query", classify_query)
    support_graph.add_node("handle_order_status", handle_order_status)
    support_graph.add_node("handle_returns", handle_returns)
    support_graph.add_node("handle_billing", handle_billing)
    support_graph.add_node("handle_product_info", handle_product_info)

    # 2. Every query starts at the classifier
    support_graph.set_entry_point("classify_query")

    # 3. Conditional fan-out: route_by_category returns the next node's name
    support_graph.add_conditional_edges("classify_query", route_by_category, HANDLERS)

    # 4. Each handler is terminal
    for handler in HANDLERS:
        support_graph.add_edge(handler, END)

    return support_graph.compile()


def save_graph_png(path: str = "docs/workflow_langgraph.png") -> str:
    """Export LangGraph's own rendering of the compiled graph to a PNG."""
    agent = build_graph()
    png = agent.get_graph().draw_mermaid_png()
    with open(path, "wb") as f:
        f.write(png)
    return path
