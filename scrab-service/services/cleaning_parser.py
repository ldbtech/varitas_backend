from bs4 import BeautifulSoup, Comment
import re 
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import re
import time

class HTMLCleaner:
    def __init__(self) -> None:
        self.irrelevant_selectors = [
            'script', 'style', 'noscript', 'meta', 'link', # Basic HTML tags to remove
            'header', 'footer', 'nav', 'aside', 'form', 'iframe', # Structural/non-content tags
            '.cnn-header', '.cnn-footer', '.ad-slot', '.advertisement', # Common ad/site-specific classes
            '.nav-menu', '.sidebar', '.related-articles', '.comments-section', # Navigation/related content
            '[class*="promo"]', '[id*="ad"]', '[class*="ad"]', # More generic ad/promo selectors
            '[id*="pop-up"]', '[class*="pop-up"]', # Pop-ups
            '[role="banner"]', '[role="navigation"]', # ARIA roles
            '.skip-link', '.visuallyhidden' # Accessibility/hidden elements that don't add value to content
        ]
      
        self.article_body_selectors = [
                'div.article__content-wrapper', # Specific to CNN
                'article',                    # HTML5 article tag
                'div#body-text',              # Common ID for article content
                'main',                       # HTML5 main tag
                'div.story-body',             # Another common pattern
                'div.content-main',           # General content div
                'div.article-body'            # Another common pattern
        ]

    def clean_html(self, html_content: str) -> Optional[str]:
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, "lxml")

        # Remove HTML comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Remove irrelevant elements based on predefined selectors
        for selector in self.irrelevant_selectors:
            for element in soup.select(selector):
                element.decompose() # Removes the tag and its contents
        
        # Attempt to find the main article body
        article_body_element = None
        for selector in self.article_body_selectors:
            article_body_element = soup.select_one(selector)
            if article_body_element:
                break # Found a potential article body, stop searching
        
        cleaned_text = ""
        if article_body_element:
            cleaned_text = article_body_element.get_text(separator='\n', strip=True)
        else:
            print("Warning: Could not find a clear article body element. Extracting all body text.")
            return soup.body.get_text(separator='\n', strip=True)

def get_dynamic_html(url:str, wait_time: int = 5) -> str:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    service = Service()

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(wait_time)
        return driver.page_source
    finally:
        driver.quit()



if __name__ == "__main__":
    url = "https://www.onlineathens.com/picture-gallery/sports/college/baseball/2025/05/30/georgia-opens-ncaa-regionals-action-against-binghamton/83944796007/"

    html_content = get_dynamic_html(url=url)


    cleaning = HTMLCleaner()

    cleaned_text = cleaning.clean_html(html_content=html_content)

    print(cleaned_text)

