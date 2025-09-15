import wikipedia

def search_wikipedia(query, sentences=5):
    try:
        summary = wikipedia.summary(query, sentences=sentences)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"Too many results found. Did you mean: {e.options[:5]}?"
    except wikipedia.PageError:
        return "Sorry, I couldn’t find anything on Wikipedia for that."
    except Exception as e:
        return f"Error: {str(e)}"
