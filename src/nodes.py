"""Graph nodes.

Every node takes the full `AgentState` and returns a partial dict of only the
keys it changed. `route_by_category` is not a node — it is the routing function
consumed by `add_conditional_edges`, and it returns the *name* of the next node.
"""

import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from . import prompts
from .data import (
    BILLING_POLICY,
    RETURN_POLICY,
    format_order_context,
    format_product_context,
)
from .state import AgentState, RouteDecision

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))

llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

# Maps the classifier's category to the node that should handle it.
ROUTE_MAP = {
    "order_status": "handle_order_status",
    "returns": "handle_returns",
    "billing": "handle_billing",
    "product_info": "handle_product_info",
}


def classify_query(state: AgentState) -> dict:
    """Entry node: classify the query into a category and a priority.

    `with_structured_output` binds the RouteDecision schema to the model, so the
    result is a validated Pydantic object instead of a string we'd have to parse.
    """
    prompt = prompts.CLASSIFICATION_PROMPT.format(customer_query=state["customer_query"])
    decision = llm.with_structured_output(RouteDecision).invoke(prompt)
    return {"category": decision.category, "priority": decision.priority}


def route_by_category(state: AgentState) -> str:
    """Routing function: pick the handler node name from the classified category."""
    return ROUTE_MAP[state["category"]]


def handle_order_status(state: AgentState) -> dict:
    """Answer order tracking and delivery questions using the orders database."""
    chain = ChatPromptTemplate.from_template(prompts.ORDER_STATUS_PROMPT) | llm
    response = chain.invoke(
        {
            "customer_query": state["customer_query"],
            "order_context": format_order_context(),
        }
    ).content
    return {"response": response}


def handle_returns(state: AgentState) -> dict:
    """Answer return, refund, and exchange requests using the return policy."""
    chain = ChatPromptTemplate.from_template(prompts.RETURNS_PROMPT) | llm
    response = chain.invoke(
        {
            "customer_query": state["customer_query"],
            "return_policy": RETURN_POLICY,
        }
    ).content
    return {"response": response}


def handle_billing(state: AgentState) -> dict:
    """Answer payment, charge, and invoice issues using the billing policy."""
    chain = ChatPromptTemplate.from_template(prompts.BILLING_PROMPT) | llm
    response = chain.invoke(
        {
            "customer_query": state["customer_query"],
            "billing_policy": BILLING_POLICY,
        }
    ).content
    return {"response": response}


def handle_product_info(state: AgentState) -> dict:
    """Answer product questions and recommendations using the catalog."""
    chain = ChatPromptTemplate.from_template(prompts.PRODUCT_INFO_PROMPT) | llm
    response = chain.invoke(
        {
            "customer_query": state["customer_query"],
            "product_context": format_product_context(),
        }
    ).content
    return {"response": response}
