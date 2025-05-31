# main.py (or wherever you want to run the scraper)
from services.scrabber_agent import ScrabberAgent

if __name__ == "__main__":
    # Example URLs (replace with actual URLs you want to scrape)
    urls_to_scrape = [
        "https://www.cnn.com/2025/05/30/politics/supreme-court-trump-deportations-parole",
    ]

    # Initialize the scraper agent
    scraper = ScrabberAgent(links=urls_to_scrape)

    # Get the articles
    articles = scraper.get_articles()

    # Process the extracted articles
    if articles:
        print("\n--- Extracted Articles Summary ---")
        for i, article in enumerate(articles):
            print(f"Article {i+1}:")
            print(f"  Title: {article.get('title', 'N/A')}")
            print(f"  Author: {article.get('author', 'N/A')}")
            print(f"  Date: {article.get('publication_date', 'N/A')}")
            print(f"  URL: {article.get('url', 'N/A')}")
            print(f"  Content Snippet: {article.get('content', 'N/A')[:150]}...") # Show first 150 chars
            print("-" * 30)
    else:
        print("\nNo articles were extracted.")

    # You can now save `articles` to a database, a JSON file, etc.
    # with open("extracted_articles.json", "w", encoding="utf-8") as f:
    #     json.dump(articles, f, indent=4, ensure_ascii=False)
    # print("\nExtracted articles saved to extracted_articles.json")