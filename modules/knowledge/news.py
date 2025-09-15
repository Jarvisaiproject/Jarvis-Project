import feedparser

def get_google_news(country="us", category=""):
    try:
        base_url = "https://news.google.com/rss"
        # Country format: hl=en-{CC}&gl={CC}&ceid={CC}:en
        url = f"{base_url}?hl=en-{country.upper()}&gl={country.upper()}&ceid={country.upper()}:en"

        if category:
            url = f"{base_url}/headlines/section/topic/{category.upper()}?hl=en-{country.upper()}&gl={country.upper()}&ceid={country.upper()}:en"

        feed = feedparser.parse(url)
        if not feed.entries:
            return [f"No top headlines found for {country.upper()} {category}"]

        results = []
        for entry in feed.entries[:5]:  # limit to 5 headlines
            results.append(f"{entry.title}\n{entry.link}")
        return results
    except Exception as e:
        return [f"Error fetching Google News: {str(e)}"]
