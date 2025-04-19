from datetime import datetime
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from timechange import timeChange
from selenium import webdriver
from post_item import PostItem

from dotenv import load_dotenv

load_dotenv()

post_xpath = os.getenv("POST_XPATH")
post_text_xpath = os.getenv("POST_TEXT")
source_path = os.getenv("SOURCE_PATH")
link_path = os.getenv("LINK_XPATH")

h_secret = " _69_ "

def search_and_get_post_link(browser: webdriver.Chrome, topic, days_ago, loop_range=1):
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
    for a in range(5):
        for l in tw_post:
            post_item = search_post_list(days_ago, l)
            if post_item:
                link_post.append(post_item)

        browser.execute_script("window.scrollTo(0,window.scrollY+4000)")
        time.sleep(5)

        tw_post = browser.find_elements(By.XPATH, post_xpath)

    # Remove duplicates while preserving order
    # Create a set to track seen posts
    seen_posts = set()
    # Create a new list for unique posts
    unique_posts = []
    
    # Iterate through all posts
    for post in link_post:
        # Convert post to string representation for comparison
        post_str = str(post)
        # If we haven't seen this post before
        if post_str not in seen_posts:
            # Add to seen posts
            seen_posts.add(post_str)
            # Add to unique posts list
            unique_posts.append(post)
    
    print(f"Found {len(link_post)} total posts")
    print(f"After removing duplicates: {len(unique_posts)} unique posts")
    
    return unique_posts

def search_post_list(days_ago, l):
    try:
        time_element = timeChange(l.find_element(By.XPATH, ".//time").get_attribute("datetime"))
    except Exception as e:
        print(e)
        return None
        
    # if datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago:
    if True:
        try:
            post_text = l.find_element(By.XPATH, post_text_xpath).text
            source_text = l.find_element(By.XPATH, source_path).text
            post_link = l.find_element(By.XPATH, link_path).get_attribute("href")
            
            return PostItem(
                source_text=source_text,
                post_text=post_text,
                time_element=time_element,
                post_link=post_link
            )
        except Exception as e:
            print(f"Error scraping post data: {e}")
            return None
    return None

