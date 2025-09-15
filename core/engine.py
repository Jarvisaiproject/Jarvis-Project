from core.memory_manager import MemoryManager
from core.history_manager import HistoryManager
from core.notes_manager import NotesManager
from core.summaries_manager import SummariesManager

from modules.knowledge.wikipedia_search import search_wikipedia
from modules.knowledge.google_search import google_search
from modules.knowledge.imdb_search import imdb_search
from modules.knowledge.crypto import get_crypto_price, get_top_cryptos, compare_cryptos
from modules.knowledge.stocks import get_stock_price, get_top_stocks, compare_stocks
from modules.knowledge.news import get_google_news


class JarvisEngine:
    def __init__(self):
        self.memory = MemoryManager()
        self.history = HistoryManager()
        self.notes = NotesManager()
        self.summaries = SummariesManager()

    def process_command(self, command: str) -> str:
        command_lower = command.lower()

        # --- Greetings ---
        if "hello" in command_lower:
            name = self.memory.get("name", None)
            response = f"Hello {name}! How can I help you today?" if name else "Hello! What’s your name?"

        # --- Introduce Jarvis ---
        elif "who are you" in command_lower or "your name" in command_lower:
            response = "I am Jarvis, your personal AI assistant."

        # --- Remember Name ---
        elif "my name is" in command_lower:
            name = command.replace("my name is", "").strip().title()
            self.memory.set("name", name)
            response = f"Nice to meet you, {name}! I’ll remember your name."

        # --- Remember Favorite Color ---
        elif "my favorite color is" in command_lower:
            color = command.replace("my favorite color is", "").strip().title()
            self.memory.set("favorite_color", color)
            response = f"Got it! Your favorite color is {color}."

        # --- Remember Hobby ---
        elif "my hobby is" in command_lower:
            hobby = command.replace("my hobby is", "").strip().title()
            self.memory.set("hobby", hobby)
            response = f"Cool! I’ll remember that your hobby is {hobby}."

        # --- Recall Memory ---
        elif "what's my favorite color" in command_lower or "whats my favorite color" in command_lower:
            response = f"Your favorite color is {self.memory.get('favorite_color', 'not set yet')}."
        elif "what's my hobby" in command_lower or "whats my hobby" in command_lower:
            response = f"Your hobby is {self.memory.get('hobby', 'not set yet')}."
        elif "what's my name" in command_lower or "whats my name" in command_lower:
            response = f"Your name is {self.memory.get('name', 'not set yet')}."

        # --- List Everything ---
        elif "what do you remember about me" in command_lower or "what do you know about me" in command_lower:
            facts = self.memory.get_all()
            response = "Here’s what I remember about you:\n" + "\n".join(
                [f"{k.capitalize()}: {v}" for k, v in facts.items()]
            ) if facts else "I don’t remember anything about you yet."

        # --- Notes Manager ---
        elif "add note" in command_lower:
            parts = command_lower.split(" ", 3)  # expect: add note daily do homework
            if len(parts) >= 4:
                _, _, category, note = parts
                self.notes.add(category, note)
                response = f"Added note to {category}: {note}"
            else:
                response = "Please specify category (daily/weekly/monthly/yearly) and the note."

        elif "show notes" in command_lower:
            notes = self.notes.get_all()
            response = "Here are your notes:\n" + "\n".join(
                [f"{cat.capitalize()}: {items}" for cat, items in notes.items()]
            )

        # --- Restore Backups ---
        elif "restore last backup memory" in command_lower:
            response = self.memory.restore_last_backup()
        elif "restore last backup history" in command_lower:
            response = self.history.restore_last_backup()
        elif "restore last backup notes" in command_lower:
            response = self.notes.restore_last_backup()
        elif "restore everything" in command_lower:
            mem_msg = self.memory.restore_last_backup()
            hist_msg = self.history.restore_last_backup()
            notes_msg = self.notes.restore_last_backup()
            response = f"{mem_msg}\n{hist_msg}\n{notes_msg}"

        # --- Wikipedia ---
        elif command_lower.startswith("search wikipedia for"):
            query = command.replace("search wikipedia for", "").strip()
            response = search_wikipedia(query)

        # --- Google Search ---
        elif command_lower.startswith("search google for"):
            query = command.replace("search google for", "").strip()
            if query.endswith("and summarize"):
                query = query.replace("and summarize", "").strip()
                results = google_search(query, summarize=True)
                if results and results[0].startswith("Summary from"):
                    text = results[0]
                    source = text.split("\n", 1)[0].replace("Summary from ", "").strip()
                    summary = text.split("\n", 1)[1].strip() if "\n" in text else ""
                    self.summaries.add(query, source, summary)
            else:
                results = google_search(query)
            response = "Here are the top results:\n" + "\n".join(results)

        # --- Summaries ---
        elif command_lower.startswith("search summaries for"):
            keyword = command.replace("search summaries for", "").strip()
            results = self.summaries.search(keyword)
            if results:
                response_lines = [f"- {r['query']} ({r['source']})" for r in results]
                response = "Here’s what I found in your saved summaries:\n" + "\n".join(response_lines)
            else:
                response = "I couldn’t find anything in your summaries matching that."

        elif "show summaries" in command_lower:
            summaries = self.summaries.get_all()
            if summaries:
                response_lines = [f"{s['time']} | {s['query']} ({s['source']})" for s in summaries]
                response = "Here are your saved summaries:\n" + "\n".join(response_lines)
            else:
                response = "You don’t have any saved summaries yet."

        elif command_lower.startswith("delete summaries for"):
            keyword = command.replace("delete summaries for", "").strip()
            deleted_count = self.summaries.delete(keyword)
            if deleted_count > 0:
                response = f"Deleted {deleted_count} summaries related to '{keyword}'."
            else:
                response = f"No summaries found for '{keyword}'."

        elif "clear summaries" in command_lower:
            deleted_count = self.summaries.clear()
            response = f"Cleared all {deleted_count} saved summaries."

        # --- Notes Delete/Clear ---
        elif command_lower.startswith("delete notes for"):
            parts = command_lower.split(" ", 3)  # e.g., delete notes for daily homework
            if len(parts) >= 4:
                category = parts[2]
                keyword = parts[3]
                deleted_count = self.notes.delete(category, keyword)
                response = f"Deleted {deleted_count} notes from {category} related to '{keyword}'."
            else:
                response = "Please specify category and keyword. Example: delete notes for daily homework."

        elif "clear notes" in command_lower:
            if "daily" in command_lower:
                deleted_count = self.notes.clear("daily")
                response = f"Cleared all {deleted_count} daily notes."
            elif "weekly" in command_lower:
                deleted_count = self.notes.clear("weekly")
                response = f"Cleared all {deleted_count} weekly notes."
            elif "monthly" in command_lower:
                deleted_count = self.notes.clear("monthly")
                response = f"Cleared all {deleted_count} monthly notes."
            elif "yearly" in command_lower:
                deleted_count = self.notes.clear("yearly")
                response = f"Cleared all {deleted_count} yearly notes."
            else:
                deleted_count = self.notes.clear()
                response = f"Cleared all {deleted_count} notes."

        # --- History Delete/Clear ---
        elif command_lower.startswith("delete history for"):
            keyword = command.replace("delete history for", "").strip()
            deleted_count = self.history.delete(keyword)
            response = f"Deleted {deleted_count} history entries related to '{keyword}'."

        elif "clear history" in command_lower:
            deleted_count = self.history.clear()
            response = f"Cleared all {deleted_count} history entries."

        # --- Memory Delete ---
        elif command_lower.startswith("forget my"):
            key = command.replace("forget my", "").strip().replace(" ", "_").lower()
            if self.memory.delete(key):
                response = f"Okay Aryan, I forgot your {key.replace('_',' ')}."
            else:
                response = f"I couldn’t find any memory stored for {key.replace('_',' ')}."

        # --- Memory Clear ---
        elif "clear memory" in command_lower:
            deleted_count = self.memory.clear()
            response = f"Cleared all {deleted_count} personal memories."

        # --- IMDB ---
        elif command_lower.startswith("search imdb for"):
            query = command.replace("search imdb for", "").strip()
            response = imdb_search(query)

        # --- Crypto ---
        elif command_lower.startswith("check crypto"):
            parts = command_lower.split()
            if len(parts) >= 3:
                coin = parts[2]
                response = get_crypto_price(coin)
            else:
                response = "Please specify a cryptocurrency (e.g., check crypto bitcoin)."

        elif "top cryptos" in command_lower:
            response = get_top_cryptos()

        # --- Stocks ---
        elif command_lower.startswith("check stock"):
            parts = command_lower.split()
            if len(parts) >= 3:
                stock = parts[2]
                response = get_stock_price(stock)
            else:
                response = "Please specify a stock (e.g., check stock apple)."

        elif "top stocks" in command_lower:
            response = get_top_stocks()

        # --- Compare Cryptos ---
        elif command_lower.startswith("compare crypto"):
            parts = command_lower.split()
            if len(parts) >= 4:
                coin1 = parts[2]
                coin2 = parts[3]
                response = compare_cryptos(coin1, coin2)
            else:
                response = "Please specify two cryptocurrencies (e.g., compare crypto bitcoin ethereum)."

        # --- Compare Stocks ---
        elif command_lower.startswith("compare stock"):
            parts = command_lower.split()
            if len(parts) >= 4:
                stock1 = parts[2]
                stock2 = parts[3]
                response = compare_stocks(stock1, stock2)
            else:
                response = "Please specify two stocks (e.g., compare stock apple tesla)."

        # --- News ---
        elif command_lower.startswith("search news for"):
            query = command.replace("search news for", "").strip()
            results = get_google_news(query, "")
            response = "Here are the latest news articles:\n" + "\n".join(results)

        elif command_lower.startswith("top news"):
            parts = command_lower.split()
            country = "us"
            category = ""

            if len(parts) == 3:
                if parts[2].lower() in [
                    "business", "world", "nation", "science", "sports", "technology",
                    "entertainment", "health"
                ]:
                    category = parts[2].lower()
                else:
                    country = parts[2].lower()

            if len(parts) == 4:
                country = parts[2].lower()
                category = parts[3].lower()

            results = get_google_news(country, category)
            response = f"Here are the top {category or 'general'} headlines from {country.upper()}:\n" + "\n".join(results)

        # --- Exit ---
        elif "bye" in command_lower or "exit" in command_lower:
            response = "Goodbye! 👋"

        # --- Default ---
        else:
            response = "I’m still learning. Can you rephrase?"

        # --- Save History ---
        self.history.add(command, response)
        return response
