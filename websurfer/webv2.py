import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def main():
    parser = argparse.ArgumentParser(description="Web Surfer")
    parser.add_argument("url", help="URL to surf")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    args = parser.parse_args()

    options = Options()
    options.headless = args.headless

    try:
        driver = webdriver.Firefox(options=options)
        driver.get(args.url)
        # Perform some actions on the webpage...
        page_source = driver.page_source
        print(page_source)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()