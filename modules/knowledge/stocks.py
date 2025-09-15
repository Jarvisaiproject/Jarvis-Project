import yfinance as yf

# Map of some popular stocks
stock_map = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "meta": "META"
}

def get_stock_price(name="apple"):
    try:
        symbol = stock_map.get(name.lower(), name.upper())
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="2d")
        if data.empty:
            return f"Could not fetch price for {name}."

        latest = data["Close"].iloc[-1]
        prev = data["Close"].iloc[-2] if len(data) > 1 else latest
        change = ((latest - prev) / prev) * 100 if prev != 0 else 0

        sign = "+" if change >= 0 else "-"
        return f"{name.title()} ({symbol}) is trading at ${latest:.2f} ({sign}{abs(change):.2f}% in 24h)"
    except Exception as e:
        return f"Error fetching stock price: {str(e)}"

def get_top_stocks():
    try:
        top_list = ["apple", "microsoft", "google", "amazon", "tesla", "meta"]
        results = [get_stock_price(s) for s in top_list]
        return "Top Stocks:\n" + "\n".join(results)
    except Exception as e:
        return f"Error fetching top stocks: {str(e)}"
    
def compare_stocks(stock1, stock2):
    price1 = get_stock_price(stock1)
    price2 = get_stock_price(stock2)
    return f"Stock Comparison:\n{price1}\n{price2}"

