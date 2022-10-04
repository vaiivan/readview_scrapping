from playwright.sync_api import sync_playwright
import asyncio
import time
import random
from pymongo import MongoClient
from datetime import datetime 
from dotenv import load_dotenv
import json
import os

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.amazon_raw_data

def main():
    with sync_playwright() as p:

        browser =  p.chromium.launch(headless=True)
        page =  browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")
        for page_number in range(33,76):
            page.goto("https://www.amazon.com/s?i=stripbooks&rh=n%3A3%2Cp_72%3A1250221011&page={}&content-id=amzn1.sym.f5c158e1-98f7-4998-94b8-d7306c066086&pd_rd_r=acb54319-5d47-4728-bd1f-878b638cf6b6&pd_rd_w=6fgAF&pd_rd_wg=iaof3&pf_rd_p=f5c158e1-98f7-4998-94b8-d7306c066086&pf_rd_r=H1V8G9MSMGC5ANN81NNR&qid=1662392519&ref=sr_pg_{}".format(page_number,page_number))
                    
            book_titles =  page.evaluate("[...document.querySelectorAll('h2>a>span')].map(v => {return v.innerText}) ")
            
            for book_title in book_titles:
                locator = page.locator("h2>a>span",has_text="{}".format(book_title))
                locator.click()
                page.wait_for_load_state('domcontentloaded')
                book = {}
                book["title"] = book_title
                try:
                    book["book_picture"] = page.evaluate("document.querySelector('#imgBlkFront').src")
                except Exception as e:
                    print("Error on picture: ",e)
                try:
                    book["genre"] = page.evaluate("document.querySelector('#wayfinding-breadcrumbs_feature_div>ul li:last-child>span>a').innerText")
                except Exception as e:
                    print("Error on genre: ",e)
                try:
                    book["author"] = page.evaluate('[...document.querySelectorAll(".author")].map( a => {return a.innerText})')
                except Exception as e:
                    print("Error on author: ",e)
                try:
                    book["book_pages"] = page.evaluate("document.querySelector('.a-carousel-card:nth-child(1) .rpi-attribute-value').innerText ")
                except Exception as e:
                    print("Error on book_pages: ",e)
                try:
                    book["publisher"] = page.evaluate("document.querySelector('.a-carousel-card:nth-child(3) .rpi-attribute-value').innerText ")
                except Exception as e:
                    print("Error on publisher: ",e)
                try:
                    book["publish_date"] = page.evaluate("document.querySelector('.a-carousel-card:nth-child(4) .rpi-attribute-value').innerText ")
                except Exception as e:
                    print("Error on publish_date: ",e)               
                try:
                    book["ISBN"] = page.evaluate("document.querySelector('.a-carousel-card:nth-last-child(2) .rpi-attribute-value').innerHTML")
                except Exception as e:
                    print("Error on ISBN: ", e)
                try:                    
                    book['reviews'] = page.evaluate('[...document.querySelectorAll(".review-text-content")].map(r => {return r.innerText})') 
                except Exception as e:
                    print("Error on reviews: ", e)
                try: 
                    book['hash'] = str(hash(json.dumps(book, sort_keys=True)))
                except Exception as e:
                    print("Error on hash: ", e)
                try:
                    book['created_at'] = datetime.now().isoformat()
                except Exception as e:
                    print("Error on created_at: ", e)
                
                print("Book", book)

                #write to MongoDB
                db.amazon_raw_data.insert_one(book)

                page.go_back()
                time.sleep(random.random()*3+30)
            print(page_number, "is finished..............." )
           
            
        
        print("im back")    
        time.sleep(3)
        browser.close()
                

if __name__ == '__main__':
    main()


