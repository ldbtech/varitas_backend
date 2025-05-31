from newsapi import NewsApiClient
from typing import List, Dict, Optional
import os 
from dotenv import load_dotenv # Import load_dotenv


load_dotenv()

class ArticleFetcher:
    def __init__(self, api_key: str) -> None:
        self.newsapi = NewsApiClient(api_key=api_key)
        self.all_articles: List[Dict] = []

    def getting_search_result(
        self, 
        search_keyword: str, 
        language: str = 'en', 
        sort_by: str = 'relevancy', 
        page_size: int = 10, 
        page: int = 1
    ) -> List[Dict]:
        if not search_keyword:
            return []

        try:
            response = self.newsapi.get_everything(
                q=search_keyword,
                language=language,
                sort_by=sort_by,
                page_size=page_size,
                page=page
            )

            self.all_articles = response.get('articles', [])
            return self.all_articles
        
        except Exception as e:
            print(f"An error occurred while fetching articles: {e}")
            return []
    
    def store_mongodb(self) -> bool:
        # TODO: Implement MongoDB storage
        return False

    def get_articles(self) -> List[Dict]:
        """
        Returns the current articles stored in the fetcher.
        """
        return self.all_articles

    def display_articles(self, articles: List[Dict]) -> None:
        """
        Prints the details of the fetched articles in a readable format.

        Args:
            articles (list): A list of article dictionaries returned by fetch_articles.
        """
        if not articles:
            print("No articles to display.")
            return

        for i, article in enumerate(articles):
            print(f"\n--- Article {i+1} ---")
            print(f"Title: {article.get('title', 'N/A')}")
            print(f"Source: {article.get('source', {}).get('name', 'N/A')}")
            print(f"Author: {article.get('author', 'N/A')}")
            print(f"Published At: {article.get('publishedAt', 'N/A')}")
            print(f"Description: {article.get('description', 'N/A')}")
            print(f"URL: {article.get('url', 'N/A')}")
            print("-" * 30)

    def get_url_references(self) -> List[str]:
        return [article.get("url") for article in self.all_articles] 
    


# --- How to use the class ---
if __name__ == "__main__":
    # IMPORTANT: Replace 'YOUR_NEWSAPI_KEY' with your actual API key
    # or even better, load it from an environment variable.
    # You can get your API key from https://newsapi.org/register
    
    # Recommended way to load API key securely:
    NEWS_API_KEY = os.getenv("NEWS_API_KEY") 
    
    # If not using environment variable, uncomment and replace directly:
    # NEWS_API_KEY = "YOUR_NEWSAPI_KEY" 

    if not NEWS_API_KEY:
        print("Please set your NewsAPI key. You can get one from https://newsapi.org/register")
        print("Set it as an environment variable 'NEWS_API_KEY' or replace 'YOUR_NEWSAPI_KEY' in the script.")
    else:
        try:
            fetcher = ArticleFetcher(api_key=NEWS_API_KEY)

            user_keyword = input("Enter a keyword to search for articles: ")

            print(f"\nFetching articles for '{user_keyword}'...")
            articles = fetcher.getting_search_result(search_keyword=user_keyword, page_size=5) # Fetch 5 articles

            fetcher.display_articles(articles)

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")            

# Create a singleton instance for the FastAPI service
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY environment variable is not set")

article_fetcher = ArticleFetcher(api_key=NEWS_API_KEY)            