from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def fetch_html_with_selenium(url: str, wait_time: int = 5) -> str:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(wait_time)  # Wait for JS to load; adjust as needed
    html = driver.page_source
    driver.quit()
    return html

if __name__ == "__main__":
    # import requests
    # response = requests.get("https://www.nytimes.com/2025/05/30/health/cdc-covid-vaccines-children-pregnant-women.html")
    url = "https://www.nytimes.com/2025/05/30/health/cdc-covid-vaccines-children-pregnant-women.html"
    html = fetch_html_with_selenium(url)
    cleaning = HTMLCleaner()
    print(cleaning.clean_html(html)) 