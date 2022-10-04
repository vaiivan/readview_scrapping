from playwright.sync_api import sync_playwright
# import asyncio
import time
import random
from pymongo import MongoClient
from datetime import datetime 
from dotenv import load_dotenv
import json
import os

# load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.books_in_print_raw_data

def main():
    

    with sync_playwright() as p:
        browser =  p.chromium.launch(headless=True,timeout=300000)
        page =  browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")
        
        for i in range(1,100):
            page.goto("https://www.goodreads.com/quotes/tag/truth?page={}".format(i))
            page.wait_for_load_state('domcontentloaded')
            print("Landed on Goodreads page {}".format(i))            
            try:    
                raw_quotes = page.evaluate('[...document.querySelectorAll(".quoteText")].map(t => {return t.innerText})')
                for raw_quote in raw_quotes:
                    quote= {}
                    quote['text'] = raw_quote
                    db.goodreads.insert_one(quote)
                    print(quote)
            except Exception as e:
                print(e)
            i=i+1
            print("Going to page {}...".format(i))
            time.sleep(random.random()*10 + 20)

        print("im back")    
        time.sleep(3)
        browser.close()        
        
if __name__ == '__main__':
    main()

