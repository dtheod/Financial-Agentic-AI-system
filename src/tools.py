import os
import requests
from langchain_core.tools import tool
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

fmp_api_key = os.environ["FMP_API_KEY"]



@tool
def get_company_profile(symbol: str) -> dict:
    """Get company profile from Financial Modeling Prep.
    
    Args:
        symbol: The stock symbol.
        
    Returns:
        Company profile data.
    """
    if not fmp_api_key:
        return "FMP API key not found."
    try:
        response = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={fmp_api_key}")
        return response.json()
    except Exception as e:
        return f"Error fetching company profile: {e}"

@tool
def get_stock_data(symbol: str) -> dict:
    """Get stock data for a given symbol using yfinance.
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
    
    Returns:
        Dictionary containing stock data and metrics
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="3mo")
        if hist.empty:
            return {"error": f"No data found for symbol {symbol}"}
        info = stock.info
        current_price = hist['Close'].iloc[-1]
        avg_volume = hist['Volume'].mean()
        price_change_30d = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
        high_52w = hist['High'].max()
        low_52w = hist['Low'].min()
        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "avg_volume": int(avg_volume),
            "price_change_30d": round(price_change_30d, 2),
            "high_52w": round(high_52w, 2),
            "low_52w": round(low_52w, 2),
            "company_name": info.get("longName", symbol),
            "sector": info.get("sector", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
        }
    except Exception as e:
        return {"error": f"Error fetching stock data: {str(e)}"}
