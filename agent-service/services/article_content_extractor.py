
from bs4 import BeautifulSoup
import requests
class ArticleContentExtractor:
    def __init__(self) -> None:
        pass

    def _extract_main_content(self, html_content: str) -> str:
        soup = BeatifulSoup(html_content, 'html_parser')

        main_content_tags = soup.fill_all(['article', 'main', 'div', 'section'], 
                                          class_=[
                                              'article-content', 'entry-content', 'post-content', 
                                              'articleBody', 'story-body', 'news-content', 'td-post-content'
                                          ])
        text_parts = []

        if main_content_tags:
            for tag in main_content_tags:
                text_parts.append(tag.get_text(separator=' ', strip=True))

        else:
            paragraph = soup.find_all('p')
            for p in paragraph:
                text_parts.append(p.get_text(strip=True))
        return ' '.join(text_parts)
    
    def get_full_articles(self, url:str) -> str:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'} # Pretend to be a common browser
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred while extracting content from {url}: {e}")
            return ""