import yfinance as yf

# Symbol map for popular cryptos
symbol_map = {
    "bitcoin": "BTC-USD",
    "ethereum": "ETH-USD",
    "dogecoin": "DOGE-USD",
    "litecoin": "LTC-USD",
    "solana": "SOL-USD",
    "cardano": "ADA-USD",
    "ripple": "XRP-USD"
}

def get_crypto_price(name="bitcoin"):
    try:
        symbol = symbol_map.get(name.lower(), name.upper() + "-USD")
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
        return f"Error fetching crypto price: {str(e)}"

def get_top_cryptos():
    try:
        top_list = ["bitcoin", "ethereum", "dogecoin", "litecoin", "solana", "cardano", "ripple"]
        results = [get_crypto_price(c) for c in top_list]
        return "Top Cryptos:\n" + "\n".join(results)
    except Exception as e:
        return f"Error fetching top cryptos: {str(e)}"
    
def compare_cryptos(coin1, coin2):
    price1 = get_crypto_price(coin1)
    price2 = get_crypto_price(coin2)
    return f"Crypto Comparison:\n{price1}\n{price2}"

