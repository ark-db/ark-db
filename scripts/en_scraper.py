from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup



_BASE_URL = "https://arknights.global"

_options = Options()
_options.add_argument("--headless")
_options.add_argument("--disable-gpu")

driver = webdriver.Firefox(
    service=Service(GeckoDriverManager().install()),
    options=_options
)
_wait = WebDriverWait(driver, 10)

driver.get(_BASE_URL)
_soup = BeautifulSoup(driver.page_source, "lxml")

EVENTS = {
    article.select_one("p.news-title").get_text(): _BASE_URL + article["href"]
    for article in _soup.select("a.news-box")
}

def get_soup(url: str) -> BeautifulSoup:
    driver.get(url)
    _wait.until(EC.presence_of_element_located((By.CLASS_NAME, "news-detail-title")))
    return BeautifulSoup(driver.page_source, "lxml")