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
import webbrowser

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

# Generate HTML results page
html_file = "results.html"
with open(html_file, "w", encoding="utf-8") as f:
    f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X Search Results for "{x_key}"</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            margin: 20px;
            background-color: #0a0a0a;
            color: #ffffff;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: #000000;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(255,255,255,0.1);
        }}
        h1 {{
            color: #1DA1F2;
            text-align: center;
            margin-bottom: 20px;
        }}
        .show-entries {{
            margin-bottom: 20px;
            color: #666;
        }}
        select {{
            background: #1a1a1a;
            color: #fff;
            border: 1px solid #333;
            padding: 5px;
            border-radius: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #222;
        }}
        th {{
            background-color: #000000;
            color: #888;
            font-weight: normal;
            text-transform: uppercase;
            font-size: 0.9em;
        }}
        tr:hover {{
            background-color: #111111;
        }}
        .status {{
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
        }}
        .status-scrapped {{
            background-color: #1b4332;
            color: #4ade80;
        }}
        .status-not-scrapped {{
            background-color: #431b1b;
            color: #f87171;
        }}
        a {{
            color: #1DA1F2;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .pagination {{
            margin-top: 20px;
            text-align: center;
            display: flex;
            justify-content: center;
            gap: 10px;
        }}
        .pagination button {{
            background: #1a1a1a;
            border: 1px solid #333;
            padding: 8px 16px;
            color: #fff;
            cursor: pointer;
            border-radius: 4px;
        }}
        .pagination button.active {{
            background: #1DA1F2;
            border-color: #1DA1F2;
        }}
        .pagination button:hover {{
            background: #222;
        }}
        .checkbox-column {{
            width: 30px;
        }}
        input[type="checkbox"] {{
            width: 16px;
            height: 16px;
            background: #1a1a1a;
            border: 1px solid #333;
        }}
        .showing-entries {{
            color: #666;
            margin-top: 20px;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>X Search Results for "{x_key}"</h1>
        <div class="show-entries">
            Show 
            <select>
                <option>25</option>
                <option>50</option>
                <option>100</option>
            </select>
            items
        </div>
        <table>
            <thead>
                <tr>
                    <th class="checkbox-column"><input type="checkbox"></th>
                    <th>Source</th>
                    <th>Post Text</th>
                    <th>Date</th>
                    <th>URL</th>
                    <th>Scrapped Status</th>
                </tr>
            </thead>
            <tbody>
''')

    # Add each result as a table row
    for post in results_dict:
        f.write(f'''
                <tr>
                    <td class="checkbox-column"><input type="checkbox"></td>
                    <td>{post['source_text']}</td>
                    <td>{post['post_text']}</td>
                    <td>{post['time_element']}</td>
                    <td><a href="{post['post_link']}" target="_blank">View Post 🔗</a></td>
                    <td><span class="status status-scrapped">Scrapped</span></td>
                </tr>
''')

    f.write(f'''
            </tbody>
        </table>
        <div class="showing-entries">
            Showing 1 to {len(results_dict)} of {len(results_dict)} posts
        </div>
        <div class="pagination">
            <button>Previous</button>
            <button class="active">1</button>
            <button>2</button>
            <button>3</button>
            <button>Next</button>
        </div>
    </div>
</body>
</html>
''')

print(f"HTML results page generated at {html_file}")

# Open the HTML file in the default browser
webbrowser.open('file://' + os.path.abspath(html_file))

# Print results to console
for post in search_results:
    print(str(post))
