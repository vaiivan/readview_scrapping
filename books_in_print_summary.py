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
login_2 = os.environ.get("LOGIN2")
password_2 = os.environ.get("PW2")

genres = ["Domestic", "Dystopia", "Epic"]

def main():    
    with sync_playwright() as p:
        
        browser =  p.chromium.launch(headless=True,timeout=300000)
        page =  browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")
        
        page.goto("https://www-booksinprint-com.ezproxy.hkpl.gov.hk/Search/Results?q=&qs=1&&op=4&ps=100")
        page.wait_for_load_state('domcontentloaded')
        print("Landed on HK library")
        are_not = page.locator("text=are not")
        are_not.click()
        time.sleep(random.random()*2 + 1)
        previous = page.locator("text=go back to previous page")
        time.sleep(random.random()*2 + 1)
        previous.click()
        page.wait_for_load_state('domcontentloaded')
        accept = page.locator("text=Accept and log in")
        print("Accepted and login")
        time.sleep(random.random()*2 + 1)
        accept.click()
        page.wait_for_load_state('domcontentloaded')
        time.sleep(random.random()*2 + 1)
        card = page.locator("#account")
        card.type(login_2, delay=100)
        pw = page.locator("#password")
        pw.type(password_2, delay=100)
        print("Password filled")
        login = page.locator(".butn-login-en",has_text="Login")
        login.click()
        time.sleep(random.random()*5 + 2)
        page.goto("https://www-booksinprint-com.ezproxy.hkpl.gov.hk/")
        page.wait_for_load_state('domcontentloaded')
        print("Landed on Books In Print")
        time.sleep(random.random()*5 + 2)
        
        for genre in genres:
            page.goto("https://www-booksinprint-com.ezproxy.hkpl.gov.hk/Search/Results?q={{{{(genre:[{0}]%20OR%20subgenre:[{1}])}}}}%20AND%20synd_profile_rec:[$ANY_VALUE$]".format(genre,genre))
            time.sleep(random.random()*5 + 2)
            page.wait_for_load_state('domcontentloaded')
            print("Landed on {}".format(genre))
            page.goto("https://www-booksinprint-com.ezproxy.hkpl.gov.hk/Search/Results?q=&qs=1&&op=4&ps=100")
            page.wait_for_load_state('domcontentloaded')
            print("100 items per page")
            
            time.sleep(random.random()*5 + 2)

            for j in range(2,4):
                page.goto("https://www-booksinprint-com.ezproxy.hkpl.gov.hk/Search/Results?q=&qs=1&&op=3&pn={}".format(j))
                titles = page.evaluate('[...document.querySelectorAll("h5 >a")].map(t => {return t.innerText})')
                print("Starting on page 2 of {}".format(j))
                time.sleep(random.random()*30 + 2)
                for title in titles:
                    try:                    
                        locator = page.locator("h5>a",has_text="{}".format(title))
                        locator.click()                    
                        page.wait_for_load_state('domcontentloaded')
                        print("I'm in")
                        time.sleep(random.random()*8 + 2)
                        try:
                            readMore = page.locator("document.querySelector('a.unbound_link.unbound_truncate_sumore')")
                            # readMore = page.locator("text= (read more)")
                            readMore.click()
                            page.wait_for_load_state('domcontentloaded')
                            print("Im trying to read more...")
                            time.sleep(random.random()*8 + 2)
                            try:
                                book = {}
                                book['summary'] = page.evaluate("document.querySelector('.unbound_lang_summary').innerText")
                                print(book['summary'])
                                print("Found read more")
                                db.summary.insert_one(book)
                            except Exception as e:
                                print("Cant find summary", e)
                        except Exception as e:
                            print("Cant find read more")
                            time.sleep(random.random()*8 + 2)
                            try:
                                book = {}
                                book['summary'] = page.evaluate("document.querySelector('.unbound_lang_summary').innerText")
                                print("Short summary")
                                print(book['summary'])
                                db.summary.insert_one(book)
                            except Exception as e:
                                print("Cant find summary", e)
                        page.go_back()
                    except Exception as e:
                        print("Going to next page...")
                        
                j=j+1
        print("im back")    
        time.sleep(3)
        browser.close()        
        
if __name__ == '__main__':
    main()


