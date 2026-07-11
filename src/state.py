"""State schema and structured-output models for the routing graph."""

from typing import Literal

from pydantic import BaseModel, Field
from typing_extensions import TypedDict

Category = Literal["order_status", "returns", "billing", "product_info"]
Priority = Literal["low", "medium", "high"]


class AgentState(TypedDict):
    """The state object that flows through every node in the graph.

    Each node reads from this dict and returns only the keys it modifies;
    LangGraph merges the returned partial state back into the whole.
    """

    customer_query: str
    category: str
    priority: str
    response: str


class RouteDecision(BaseModel):
    """Classification result for a customer support query.

    Used with `llm.with_structured_output(...)` so the model is forced to
    return one of the allowed categories/priorities rather than free text.
    """

    category: Category = Field(description="The category of the customer query")
    priority: Priority = Field(
        description="The priority level based on urgency and business impact"
    )
