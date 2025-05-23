import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import time

def navigate2url(url, headless=False, timeout=0):
    options = Options()
    options.headless = headless
    try:
        driver = webdriver.Firefox(options=options)
        res = driver.get(url)
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

def main():
    parser = argparse.ArgumentParser(description="Web Surfer")
    parser.add_argument("--url", help="URL to surf", default="https://www.duckduckgo.com")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    args = parser.parse_args()
    
    print(args)

    navigate2url(args.url, args.headless)    

if __name__ == "__main__":
    main()