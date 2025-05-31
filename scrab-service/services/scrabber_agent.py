# scrabber_agent.py
import requests
from typing import List
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Import the Article TypedDict from your models module
from models.article import Article

# Load environment variables from .env file (e.g., GOOGLE_API_KEY)
load_dotenv()

class ScrabberAgent:
    """
    A class that handles the scraping of article content from multiple URLs
    using the Gemini API for structured data extraction.
    """
    def __init__(self, links: List[str]) -> None:
        """
        Initializes the ScrabberAgent with a list of URLs to scrape.
        
        Args:
            links (List[str]): A list of URLs pointing to articles to scrape.
        """
        self.links = links
        # This list will store all extracted Article dictionaries
        self.all_articles: List[Article] = []

        # Initialize Gemini model
        try:
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            # Optional: Test a small prompt to ensure API key is valid
            # self.gemini_model.generate_content("hello") 
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini API. Check GOOGLE_API_KEY: {e}")

    def get_articles(self) -> List[Article]:
        """
        Fetches HTML content from each URL, extracts article details using Gemini,
        and aggregates them into a single list.
        
        Returns:
            List[Article]: A list of all extracted article dictionaries.
        """
        print(f"Starting scraping process for {len(self.links)} URLs...")
        for url in self.links:
            print(f"\n--- Processing URL: {url} ---")
            try:
                # Make an HTTP GET request to fetch the HTML content
                # Added timeout for robustness and raise_for_status for immediate HTTP error handling
                response = requests.get(url=url, timeout=15) # Increased timeout slightly
                print(response.text, "\n\n")
                response.raise_for_status() # Raises HTTPError for 4xx/5xx responses
                
                # Pass the HTML content to the internal scraper agent
                # The _scrabber_agent returns a List[Article]
                extracted_data_for_url = self._scrabber_agent(
                    html_content=response.text, 
                    source_url=url
                )
                
                # If Gemini successfully extracted articles, add them to the main list
                if extracted_data_for_url:
                    self.all_articles.extend(extracted_data_for_url)
                    print(f"Successfully extracted {len(extracted_data_for_url)} article(s) from {url}")
                else:
                    print(f"No article data extracted from {url}. It might not be an article page or content is too complex.")

            except requests.exceptions.HTTPError as e:
                print(f"ERROR: HTTP Error {e.response.status_code} for {url}: {e.response.reason}")
            except requests.exceptions.ConnectionError as e:
                print(f"ERROR: Connection Error for {url}: {e}")
            except requests.exceptions.Timeout as e:
                print(f"ERROR: Timeout occurred while fetching {url}: {e}")
            except requests.exceptions.RequestException as e:
                print(f"ERROR: An unexpected request error occurred for {url}: {e}")
            except Exception as e:
                print(f"ERROR: An unhandled exception occurred for {url}: {e}")
        
        print("\n--- Scraping process completed ---")
        print(f"Total articles extracted: {len(self.all_articles)}")
        return self.all_articles

    def _scrabber_agent(self, html_content: str, source_url: str) -> List[Article]:
        """
        Internal method to extract article content from HTML using the Gemini API.
        This method sends HTML content to Gemini with specific instructions
        to extract structured article details.
        
        Args:
            html_content (str): Raw HTML content from the webpage.
            source_url (str): The URL from which the HTML content was fetched.
                              Used to help Gemini populate the 'url' field if no canonical URL is found.
            
        Returns:
            List[Article]: A list of extracted article dictionaries. Returns an empty list
                           if no articles are found or if an error occurs during extraction.
        """
        if not html_content:
            print("Warning: Received empty HTML content for scraping.")
            return []
        
        article_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The prominent headline or title of the article."},
                    "author": {"type": ["string", "null"], "description": "The name(s) of the article's author(s). If multiple, combine into a single string. Null if not found."},
                    "publication_date": {"type": ["string", "null"], "description": "The exact publication date of the article in YYYY-MM-DD or similar format. Null if not found."},
                    "content": {"type": "string", "description": "The complete, main body text of the article, excluding non-article elements."},
                    "url": {"type": ["string", "null"], "description": "The canonical URL of the article. Prioritize from HTML meta tags, otherwise use source_url. Null if not found."},
                },
                "required": ["title", "content"] # Define required fields based on your Article TypedDict
            }
        }
        
        # The detailed context (system instruction) to guide Gemini's extraction.
        # It explicitly defines the task, desired fields, and expected JSON output format.
            # The detailed context (system instruction) to guide Gemini's extraction.
        context = f"""
        You are an expert at extracting structured information from raw HTML content.
        Your primary task is to carefully parse the provided HTML and extract the main article details.
        
        For each identifiable article found within the HTML, extract the following specific information:
        - `title`: The prominent headline or title of the article.
        - `author`: The name(s) of the article's author(s). If multiple authors are listed, combine their names into a single string (e.g., "John Doe and Jane Smith"). If no author is explicitly mentioned, return `null`.
        - `publication_date`: The exact publication date of the article. Extract the most precise date possible (e.g., "YYYY-MM-DD", "Month DD, YYYY", or "YYYY-MM-DD HH:MM:SS"). If the date is not found, return `null`.
        - `content`: The complete, main body text of the article. It is critical to exclude any non-article-body elements such as website headers, footers, navigation menus, sidebars, advertisements, related article links, comments sections, or short introductory snippets outside the main content flow. Focus only on the core narrative text.
        - `url`: The canonical URL of the article. Prioritize extracting this from `<link rel="canonical">` or Open Graph (`og:url`) meta tags within the HTML. If neither is present, use the `source_url` provided in the user message. If still not found, return `null`.

        The output must be a JSON array (list) of objects. Each object in the array must strictly conform to the following JSON schema:
        {json.dumps(article_schema, indent=2)}

        If you cannot confidently extract any article content from the HTML, return an empty JSON array: `[]`.
        Do NOT include any additional text or conversational remarks in your response, only the JSON.
        """
        
        # The user message combines the instruction with the actual HTML content
        # and the source_url to assist Gemini in finding the URL field.
        user_message = f"Please extract article details from the following HTML. The source URL for this content is: {source_url}\n\nHTML Content:\n{html_content}"

        try:
            # Generate content using the Gemini model, forcing JSON output
            response = self.gemini_model.generate_content(
                [context, user_message],
                generation_config=genai.types.GenerationConfig(
                    response_mime_type='application/json' # Ensures Gemini attempts to return valid JSON
                ),
                # Optional: request_options to set timeout for Gemini API call
                # request_options={'timeout': 180} 
            )

            # Check if Gemini returned any text, which should be JSON
            if not hasattr(response, 'text') or not response.text:
                print(f"Warning: Gemini response was empty or did not contain text for URL: {source_url}")
                return []
            
            # Attempt to parse the JSON string from Gemini's response
            extracted_raw_data = json.loads(response.text)
            
            # Validate that the parsed data is a list (as requested in the prompt)
            if not isinstance(extracted_raw_data, list):
                print(f"Warning: Gemini returned an unexpected type ({type(extracted_raw_data)}), expected a list for URL: {source_url}. Raw: {response.text[:200]}...")
                return []

            # Validate each item in the list against the Article TypedDict structure
            validated_articles: List[Article] = []
            for item in extracted_raw_data:
                # Basic validation: check if it's a dict and has at least a title/content
                if isinstance(item, dict) and 'title' in item and 'content' in item:
                    # You could add more sophisticated validation here if needed
                    # For TypedDict, Python's type checker would ideally handle this
                    validated_articles.append(item)
                else:
                    print(f"Warning: Skipping malformed article item from Gemini for {source_url}: {item}")
            
            return validated_articles

        except json.JSONDecodeError as e:
            print(f"ERROR: Gemini did not return valid JSON for {source_url}. Error: {e}\nRaw response (first 500 chars): {response.text[:500]}...")
            return []
        except Exception as e:
            print(f"ERROR: An unhandled exception occurred during Gemini extraction for {source_url}: {e}")
            return []