from datetime import datetime, timedelta
import os
import pickle
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from get_chrome_driver import GetChromeDriver
from selenium.webdriver.common.by import By
from login import login
from post_Link import search_and_get_post_link
from post_item import PostItem

def load_cookies(driver: webdriver.Chrome):
        cookies_path="x_cookies.pkl"
        try:
            with open(cookies_path, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            print("Cookies loaded successfully.")
            driver.refresh()
        except FileNotFoundError:
            print("Cookies file not found.")

def save_cookies(driver):
        cookies_path="x_cookies.pkl"
        with open(cookies_path, "wb") as file:
            pickle.dump(driver.get_cookies(), file)
        print(f"Cookies saved to {cookies_path}")


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
print(BASE_DIR)
CHROMEDRIVER_PATH = "chromedriver_linux64"
CHROME_HEADLESS = False
chrome_dir = BASE_DIR + "/" + CHROMEDRIVER_PATH
chrome_file_path = chrome_dir + "/chromedriver"
option = webdriver.ChromeOptions()
option.add_argument("--disable-notifications")
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-shm-usage")
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option("useAutomationExtension", False)
option.add_experimental_option("detach", False)
option.add_argument("--disable-infobars")
service = Service(executable_path=chrome_file_path)
print(chrome_file_path)
url = "https://x.com"


days_ago = datetime.now() - timedelta(days=7)
scroll = 0
x_key = "#বাংলাদেশ"

try:
    browser =  webdriver.Chrome(service=service, options=option) # for docker developement
    # browser = webdriver.Chrome()  # For window developement
    browser.get(url)
except Exception as e:
    print("Selenium session is not Created !", e)
    if os.path.exists(chrome_file_path):
        os.remove(chrome_file_path)
        print(f"Removed {chrome_file_path} file!")
    download_driver = GetChromeDriver()
    download_driver.auto_download(extract=True, output_path=chrome_dir)
    print(
        f"Downloaded chrome driver for the chrome version {download_driver.matching_version()}!"
    )
    browser = webdriver.Chrome(service=service, options=option)
    browser.get(url)

browser.maximize_window()
browser.implicitly_wait(5)
# Login
try:
    load_cookies(browser)
    time.sleep(5)
    browser.find_element(
            By.XPATH, '//*[@id="react-root"]//header'
        )
    print("Already Logged In >>>>>>")
except Exception as e:
        print("Trying to Log In ")
        try:
            login(
                browser,
                "aleya98337",
                "Test@123!",
            )
            browser.find_element(
                By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div'
            )
            print("Logged In Successfull >>>>>>")
        except Exception as e:
            print("Error Log In: ", e)
            print("Log In Failed! Manually Log In ....")
            input("Press Enter To Continue......")
        save_cookies(browser)

search_results = search_and_get_post_link(browser, x_key, days_ago, scroll)

# Convert PostItem objects to dictionaries
results_dict = [{
    "source_text": post.source_text,
    "post_text": post.post_text,
    "time_element": post.time_element,
    "post_link": post.post_link
} for post in search_results]

# Write to JSON file
output_file = "search_results.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results_dict, f, ensure_ascii=False, indent=4)

print(f"Search results written to {output_file}")

# Print results to console
for post in search_results:
    print(str(post))
