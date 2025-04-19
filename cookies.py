import pickle
from selenium import webdriver

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
