import requests
import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import openagents

class WebSurfer:
    def __init__(self, verbose=False, dump=False):
        self.session = requests.Session()
        self.verbose = verbose
        self.dump = dump
        
        if verbose:
            print("WebSurfer initialized")
            

    def get(self, url):
        if self.verbose:
            print(f"Fetching {url}")
        return self.session.get(url)
    
    def post(self, url, data):
        if self.verbose:
            print(f"Posting to {url}")
        return self.session.post(url, data=data)
    
    def get_content(self, response):
        content = response.content
        if self.verbose:
            print("Getting response content")
            print(content)     
            
        if self.dump:
            
            with open("webdump.html", "wb") as f:
                f.write(content) 
                
        return content
    

if __name__ == "__main__":
    args = argparse.ArgumentParser()

    args.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging", default=False)
    args.add_argument("--model", "-m", choices=["llama3.2", "deepseek-r1:7b"], help="LLM model to use", default="llama3.2")
    args.add_argument("--url", "-u", help="URL to fetch", default="https://www.duckduckgo.com")
    args.add_argument("--dump", "-d", action="store_true", help="Dump the response content in webdump folder", default=False)

    args = args.parse_args()
        
    ws = WebSurfer(args.verbose,args.dump)
    response = ws.get(args.url)
    content = ws.get_content(response)
    
        
    
    