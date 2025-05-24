# from base import navigate2url
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import time

def navigate2url(url, headless=False, timeout=0):
    options = Options()
    options.headless = headless
    try:
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        # # Perform some actions on the webpage...
        page_source = driver.page_source
        print(driver.title) 
        # print(page_source)
        return driver
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        time.sleep(timeout)
        driver.quit()


def search_duckduckgo(query):
    url = f"https://duckduckgo.com/?q={query}"
    try:
        driver = navigate2url(url)
    
        # print(driver.title)
        # print(driver)
        links = driver.find_elements(By.CLASS_NAME, "a")
        print(driver.title)
        print(links)
        return links

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
    
def search_google(query):
    url = f"https://google.com/?q={query}"
    driver = navigate2url(url)
    
    print(driver.title)
    
if __name__ == "__main__":
    query = "What's the latest news about OpenAI's new models?"
    links = search_duckduckgo(query)
    
    
    
    for link in links:
        print(link.text)