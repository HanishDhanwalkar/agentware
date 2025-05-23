from base import navigate2url

def search_duckduckgo(query):
    url = f"https://duckduckgo.com/?q={query}"
    driver = navigate2url(url)
    
    # print(driver.title)
    print(driver)
    
def search_google(query):
    url = f"https://google.com/?q={query}"
    driver = navigate2url(url)
    
    print(driver.title)
    
if __name__ == "__main__":
    query = "What's the latest news about OpenAI's new models?"
    search_duckduckgo(query)