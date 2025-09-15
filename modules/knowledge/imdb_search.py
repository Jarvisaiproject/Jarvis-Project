from imdb import IMDb

ia = IMDb()

def imdb_search(title, top_n=3):
    try:
        movies = ia.search_movie(title)
        if not movies:
            return f"No results found for '{title}'."

        results = []
        for movie in movies[:top_n]:  # take top N matches
            movie_id = movie.movieID
            movie = ia.get_movie(movie_id)

            title = movie.get('title', 'Unknown Title')
            year = movie.get('year', 'Unknown Year')
            plot = movie.get('plot', ["No summary available."])[0]

            # Shorten the summary
            short_summary = plot.split("::")[0]
            if len(short_summary) > 250:
                short_summary = short_summary[:250] + "..."

            results.append(f"{title} ({year})\nSummary: {short_summary}")

        return "\n\n".join(results)

    except Exception as e:
        return f"Error fetching IMDb data: {str(e)}"
