from playwright.sync_api import sync_playwright
# import asyncio
import time
import random
from pymongo import MongoClient
from datetime import datetime 
from dotenv import load_dotenv
import json
import os
import math

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.books_in_print_raw_data

def main():
    with sync_playwright() as p:

        browser =  p.chromium.launch(headless=True)
        page =  browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")
        for page_number in range(4,10):
            page.goto("https://www.amazon.com/s?i=stripbooks&rh=n%3A3377866011%2Cp_72%3A1250221011&page={}&content-id=amzn1.sym.f5c158e1-98f7-4998-94b8-d7306c066086&pd_rd_r=1e4ea41b-cc04-4ba0-b9e1-9a088f167f6d&pd_rd_w=RtBea&pd_rd_wg=AGmVh&pf_rd_p=f5c158e1-98f7-4998-94b8-d7306c066086&pf_rd_r=CVZ3YXZ365F590E8YV1X&qid=1664178157&ref=sr_pg_{}".format(page_number,page_number))
            print("Landed on {}".format(page_number))
                    
            book_titles =  page.evaluate("[...document.querySelectorAll('h2>a>span')].map(v => {return v.innerText}) ")
            print("Found these titles", book_titles)
            time.sleep(random.random()*30+20)
            
            for book_title in book_titles:
                locator = page.locator("h2>a>span",has_text="{}".format(book_title))
                locator.click()
                page.wait_for_load_state('domcontentloaded')
                print("Landed on title: ", book_title)
                book = {}
                book["title"] = book_title
                try:                    
                    book['reviews'] = page.evaluate('[...document.querySelectorAll(".review-text-content")].map(r => {return r.innerText})') 
                except Exception as e:
                    print("Error on reviews: ", e)
                
                print("Book", book)

                #write to MongoDB
                db.review.insert_one(book)

                page.go_back()
                time.sleep(random.random()*30+20)
            print(page_number, "is finished..............." )
           
            
        
        print("im back")    
        time.sleep(3)
        browser.close()
        
        
if __name__ == '__main__':
    main()
