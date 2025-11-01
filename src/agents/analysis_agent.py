from langchain_core.messages import AIMessage, HumanMessage
from src.models import llm
from src.logger import get_logger

logger = get_logger(__name__)

def node(state: dict) -> dict:
    """Synthesizes a financial analysis from the research conversation."""
    logger.info("--- AGENT: Analyst ---")
    
    # Get the full message history
    messages = state["messages"]
    
    # Create the prompt for the analysis agent
    prompt = f"""You are a senior financial analyst. Based on the following research conversation, 
    provide a detailed financial analysis and recommendation for the stock {state['symbol']}.
    
    The analysis should include:
    1.  **Executive Summary**: A brief overview of the stock and your recommendation.
    2.  **Company Profile**: Description of the company, its business, and market position.
    3.  **Financial Health**: Key financial metrics, recent performance, and price trends.
    4.  **News & Market Sentiment**: Summary of recent news and overall market sentiment.
    5.  **Risk Assessment**: Potential risks and headwinds.
    6.  **Investment Thesis**: A clear recommendation (Buy, Hold, Sell) with a well-reasoned justification.
    
    Be thorough, insightful, and use a professional tone.

    Research Conversation:
    {state["messages"]}
    """
    
    # Invoke the LLM to generate the final analysis
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Update the state with the final analysis
    state["analysis"] = response.content
    state["messages"].append(AIMessage(content="Analysis complete."))
    
    return state