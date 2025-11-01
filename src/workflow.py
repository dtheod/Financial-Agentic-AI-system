from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import operator
from src.agents.data_collection_agent import node as data_collection_node
from src.agents.analysis_agent import node as analysis_node
from typing import TypedDict, List, Annotated


# Define the state
class FinancialAdvisorState(TypedDict):
    """State for the financial advisor workflow."""
    symbol: str
    messages: Annotated[List, operator.add]
    stock_data: dict
    analysis: str


def create_financial_advisor_workflow():
    """Create and compile the financial advisor workflow."""
    workflow = StateGraph(FinancialAdvisorState)
    
    # Add nodes
    workflow.add_node("data_collection", data_collection_node)
    workflow.add_node("analysis", analysis_node)
    
    # Define the flow
    workflow.add_edge(START, "data_collection")
    workflow.add_edge("data_collection", "analysis")
    workflow.add_edge("analysis", END)
    
    app = workflow.compile()
    png_graph = app.get_graph().draw_mermaid_png()
    with open("workflow_graph.png", "wb") as f:
        f.write(png_graph)

    # Compile the workflow
    return app

