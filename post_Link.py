from datetime import datetime
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from timechange import timeChange
from selenium import webdriver

from dotenv import load_dotenv

load_dotenv()

post_xpath = os.getenv("POST_XPATH")
post_text_xpath = os.getenv("POST_TEXT")
source_path = os.getenv("SOURCE_PATH")
link_path = os.getenv("LINK_XPATH")

h_secret = " _69_ "

def search_and_get_post_link(browser: webdriver.Chrome, topic,days_ago,loop_range=1):
    link_post = []
    elem = browser.find_element(By.CSS_SELECTOR, ".r-30o5oe")
    elem.click()
    elem.clear()
    elem.send_keys(Keys.CONTROL + "a")
    elem.send_keys(Keys.DELETE)
    elem.send_keys(topic)

    # using keys to send special KEYS
    elem.send_keys(Keys.RETURN)

    print("Search Successful")
    time.sleep(5)
    tw_post = browser.find_elements(
        By.XPATH, post_xpath
    )
    # link_post += [l.get_attribute("href") for l in tw_post]
    for a in range(5):
        for l in tw_post:
            search_post_list(days_ago, link_post, l)

        browser.execute_script("window.scrollTo(0,window.scrollY+4000)")
        time.sleep(5)

        tw_post = browser.find_elements(By.XPATH, post_xpath)



    link_post = list(dict.fromkeys(link_post))

    print(len(link_post))
    [print(l) for l in link_post]
    # print("Key:")
    return link_post

def search_post_list(days_ago, link_post, l):
    try:
        time_element = timeChange(l.find_element(By.XPATH, ".//time").get_attribute("datetime")) #Post Time
    except Exception as e:
        print(e)
        
    if datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago:
        link_post.append(l.get_attribute("href"))
        print("Link Appended.")
    else:
        print(datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago)
        
    try:
        post_text = l.find_element(By.XPATH,post_text_xpath).text
        print(post_text)
    except:
        print("Couldn't Scrap Post Text")

    try:
        source_text = l.find_element(By.XPATH,source_path).text
        print(source_text)
    except Exception as e:
        print("Couldn't Scrap Source Text:", e)

    try:
        post_link = l.find_element(By.XPATH,link_path).get_attribute("href")
        print(post_link)
    except Exception as e:
        print("Couldn't Scrap Post Link:", e)
        
    link_post.append(source_text+ h_secret + post_text + h_secret + time_element + h_secret + post_link)

