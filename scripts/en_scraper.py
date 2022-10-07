import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup

BASE_URL = "https://arknights.global"

os.environ['WDM_LOCAL'] = '1'

driver = webdriver.Firefox(
    service=Service(GeckoDriverManager(path="./").install())
)

wait = WebDriverWait(driver, 10)

driver.get(BASE_URL)

soup = BeautifulSoup(driver.page_source,
                     "lxml")

def get_soup(url: str) -> BeautifulSoup:
    driver.get(url)
    #driver.refresh()
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "news-detail-title")))
    except TimeoutException:
        print("Timed out")
    return BeautifulSoup(driver.page_source, "lxml")



events = {
    article.select_one("p.news-title").get_text(): BASE_URL + article["href"]
    for article in soup.select("a.news-box")
}