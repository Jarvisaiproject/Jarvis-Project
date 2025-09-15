from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

def google_search(query, num_results=5, summarize=False):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                results.append(r["href"])

        if not results:
            return ["No results found."]

        # If summarize option is requested
        if summarize:
            first_url = results[0]
            try:
                page = requests.get(first_url, timeout=5)
                soup = BeautifulSoup(page.text, "html.parser")
                # Extract visible text
                paragraphs = [p.get_text() for p in soup.find_all("p")]
                text = " ".join(paragraphs[:5])  # take first 5 paragraphs
                summary = text.strip()[:500] + "..." if len(text) > 500 else text.strip()
                return [f"Summary from {first_url}:\n{summary}"]
            except Exception as e:
                return [f"Found link but failed to summarize: {str(e)}"]

        return results

    except Exception as e:
        return [f"Error: {str(e)}"]
