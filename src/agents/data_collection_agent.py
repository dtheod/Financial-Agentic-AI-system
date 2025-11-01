from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from src.tools import get_company_profile, get_stock_data
from src.models import llm
from src.logger import get_logger

logger = get_logger(__name__)

# List of tools for the agent to use
tools = [get_company_profile, get_stock_data]

# Bind the tools to the LLM
llm_with_tools = llm.bind_tools(tools)

def node(state: dict) -> dict:
    """Runs the data collection agent to gather information about a stock.
    
    This agent is a "stateful" agent, meaning it can call tools sequentially
    until it has enough information to proceed.
    """
    logger.info("--- AGENT: Data Collector ---")
    
    # The first message is the initial user query, which we will evolve
    messages = [HumanMessage(content=f"Research the stock {state['symbol']}. Find its current price, recent news, and company profile.")]
    
    # Max number of tool calls to prevent infinite loops
    max_iterations = 5
    
    for i in range(max_iterations):
        # Invoke the LLM with the current messages
        logger.info(f"  [Round {i+1}] Invoking LLM with {len(messages)} messages...")
        response = llm_with_tools.invoke(messages)
        
        # If the LLM responds without calling a tool, we're done
        if not response.tool_calls:
            logger.info("  [Round {i+1}] LLM decided to stop.")
            messages.append(response)
            break
        
        # Otherwise, add the tool calls to the message history
        messages.append(response)
        
        # Invoke the tools and add the results to the message history
        logger.info(f"  [Round {i+1}] LLM wants to call {len(response.tool_calls)} tools...")
        for tool_call in response.tool_calls:
            logger.info(f"    - Calling tool: {tool_call['name']} with args: {tool_call['args']}")
            tool_to_call = next(t for t in tools if t.name == tool_call["name"])
            tool_output = tool_to_call.invoke(tool_call["args"])
            messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))

    # Update the state with the final messages and a summary
    state["messages"] += messages
    state["stock_data"] = {"research_summary": messages[-1].content}
    
    return state
