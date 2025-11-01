
from src.workflow import create_financial_advisor_workflow
from langchain_core.messages import HumanMessage
from src.logger import get_logger

logger = get_logger(__name__)

def main(symbol: str):

    # Create the workflow
    advisor = create_financial_advisor_workflow()
    
    # Initialize state
    initial_state = {
        "symbol": symbol.upper(),
        "messages": [HumanMessage(content=f"Analyze stock: {symbol}")],
        "stock_data": {},
        "analysis": ""
    }
    
    # Stream the workflow's execution for real-time logging
    final_state = None
    for state_chunk in advisor.stream(initial_state):
        # The state_chunk is a dictionary containing the output of the last node that was run
        # and the node's name.
        node_name = list(state_chunk.keys())[0]
        node_output = list(state_chunk.values())[0]
        
        logger.info(f"--- Node: {node_name} ---")
        logger.info(f"  Output: {node_output}")
        
        final_state = node_output

    logger.info("\n--- FINAL ANALYSIS ---")
    logger.info(final_state["analysis"])
    
    return final_state


if __name__ == "__main__":
    main(symbol = "AAPL")
