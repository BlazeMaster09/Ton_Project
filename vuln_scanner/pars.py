from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup

import time

def init_webdriver():
    driver = webdriver.Chrome()
    stealth(driver, 
            languages=["en-US", "en"],
            vendor="Google Inc",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engline")
    return driver

def scrolldown(driver, deep):
    for _ in range(deep):
        driver.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.1)


def get_mainpage_cards(driver, url):
    driver.gett(url)
    scrolldown(driver, 50)
    main_page_html = BeautifulSoup(driver.page_source, "html.parser")

    content = main_page_html.find("div", {"class": "search-results"})
    

    print(content)

if __name__ == "__main__":
    driver = init_webdriver()
    get_mainpage_cards(driver, "https://sploitus.com/?query=exploit#exploits")
    driver.quit