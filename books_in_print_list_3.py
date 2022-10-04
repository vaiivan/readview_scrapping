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
login_3 = os.environ.get("LOGIN3")
password_3 = os.environ.get("PW3")

genres = ["Literary", "Memoir", "Mystery", "Noir", "NonFiction", "Political", "Psychological","Religious","Romance","Saga","Satire","Science","Sociological","Suspense","Thriller","War"]

def main():    
    with sync_playwright() as p:
        
        browser =  p.chromium.launch(headless=False,timeout=300000)
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
        card.type(login_3, delay=100)
        pw = page.locator("#password")
        pw.type(password_3, delay=100)
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
            page.wait_for_load_state('domcontentloaded')
            time.sleep(random.random()*5 + 2)
            print("Landed on {}".format(genre))
            page.goto("https://www-booksinprint-com.ezproxy.hkpl.gov.hk/Search/Results?q=&qs=1&&op=4&ps=100")
            page.wait_for_load_state('domcontentloaded')
            print("100 items per page")
            
            max_page = int(math.floor(random.random()*10+5))
            print("max_page: ", max_page)

            time.sleep(random.random()*5 + 2)
            
            for j in range(2,max_page):
                page.goto("https://www-booksinprint-com.ezproxy.hkpl.gov.hk/Search/Results?q=&qs=1&&op=3&pn={}".format(j))
                titles = page.evaluate('[...document.querySelectorAll("h5 >a")].map(t => {return t.innerText})')
                print("Starting on page {} of {}".format(j, max_page))
                time.sleep(random.random()*30 + 2)
                for k in range(len(titles)-1):
                    try:
                        page.evaluate("document.querySelectorAll('.contentAlignment')[{}].childNodes[5].childNodes[0].childNodes[1].innerText".format(k))
                        book = {}
                        try:
                            book['title'] = titles[k]
                        except Exception as e:
                            print("Error on title", e)
                        try:
                            book['book_picture'] = page.evaluate("document.querySelectorAll('img.coverImage')[{}].src".format(k))
                        except Exception as e:
                            print("Error on book_picture", e)   
                        try:
                            book['genre'] = genre
                        except Exception as e:
                            print("Error on genre", e)
                        try:
                            book['author'] = page.evaluate("document.querySelectorAll('.contentAlignment')[{}].childNodes[5].childNodes[0].childNodes[1].innerText".format(k))
                        except Exception as e:
                            print("Error on author", e)
                        try:
                            book['publisher'] = page.evaluate("document.querySelectorAll('.contentAlignment')[{}].childNodes[5].childNodes[2].childNodes[5].childNodes[1].innerText".format(k))
                        except Exception as e:
                            print("Error on publisher", e)
                        try:
                            book['publish_date'] = page.evaluate("document.querySelectorAll('.contentAlignment')[{}].childNodes[5].childNodes[2].childNodes[6].childNodes[1].innerText".format(k))
                        except Exception as e:
                            print("Error on publish_date", e)
                        try:
                            book['ISBN'] = page.evaluate("document.querySelectorAll('.contentAlignment')[{}].childNodes[5].childNodes[2].childNodes[1].childNodes[1].innerText".format(k))
                        except Exception as e:
                            print("ISBN", e)
                        try:
                            book['created_at'] = datetime.now().isoformat()
                        except Exception as e:
                            print("Error on created_at: ", e)
                        print("Book" ,book)
                        db.amazon_raw_data.insert_one(book)

                    except Exception as e:                
                        book = {}
                        try:
                            book['title'] = titles[k]
                        except Exception as e:
                            print("Error on title", e)
                        try:
                            book['book_picture'] = page.evaluate("document.querySelectorAll('img.coverImage')[{}].src".format(k))
                        except Exception as e:
                            print("Error on book_picture", e)   
                        try:
                            book['genre'] = genre
                        except Exception as e:
                            print("Error on genre", e)
                        try:
                            book['author'] = page.evaluate("document.querySelectorAll('.contentAlignment')[{}].childNodes[3].childNodes[0].childNodes[1].innerText".format(k))
                        except Exception as e:
                            print("Error on author", e)
                        try:
                            book['publisher'] = page.evaluate("document.querySelectorAll('.contentAlignment')[{}].childNodes[3].childNodes[2].childNodes[5].childNodes[1].innerText".format(k))
                        except Exception as e:
                            print("Error on publisher", e)
                        try:
                            book['publish_date'] = page.evaluate("document.querySelectorAll('.contentAlignment')[{}].childNodes[3].childNodes[2].childNodes[6].childNodes[1].innerText".format(k))
                        except Exception as e:
                            print("Error on publish_date", e)
                        try:
                            book['ISBN'] = page.evaluate("document.querySelectorAll('.contentAlignment')[{}].childNodes[3].childNodes[2].childNodes[1].childNodes[1].innerText".format(k))
                        except Exception as e:
                            print("ISBN", e)
                        try:
                            book['created_at'] = datetime.now().isoformat()
                        except Exception as e:
                            print("Error on created_at: ", e)
                        print("Book" ,book)
                        db.amazon_raw_data.insert_one(book)
                j=j+1
        print("im back")    
        time.sleep(3)
        browser.close()        
        
if __name__ == '__main__':
    main()

