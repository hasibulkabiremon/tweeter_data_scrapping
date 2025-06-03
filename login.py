import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginException(Exception):
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message
        super().__init__(self.message)

class UsernameException(LoginException):
    def __init__(self, message: str = "Username not found"):
        super().__init__(False, message)

class WrongPasswordException(LoginException):
    def __init__(self, message: str = "Wrong Username/password"):
        super().__init__(False, message)

class SuspiciousLoginException(LoginException):
    def __init__(self, message: str = "Suspicious login prevented"):
        super().__init__(False, message)

class LoginFailedException(LoginException):
    def __init__(self, message: str = "Login failed"):
        super().__init__(False, message)

def login(browser, user_name, user_pass):
    try:
        login = browser.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")
        login.click()
        print("Login in Twitter")
        time.sleep(5)

        user = browser.find_element(By.CSS_SELECTOR, ".r-30o5oe")
        user.send_keys(user_name)

        next = browser.find_element(By.XPATH, "//span[text()='Next']")
        next.click()

        try:
            wait = WebDriverWait(browser, 5)
            cred_error = wait.until(EC.presence_of_element_located((By.XPATH, os.getenv('CREDENTIAL_ERROR_MESSAGE'))))
            print(str(cred_error.text))
            "hello" + 123
        except Exception as e:
            print("Username Exception type:", type(e).__name__)
            if type(e).__name__ == "TypeError":
                raise UsernameException(str(cred_error.text))
            else:
                pass

        time.sleep(5)
        passw = browser.find_element(By.CSS_SELECTOR, ".r-homxoj")
        passw.send_keys(user_pass)
        time.sleep(5)
        logIn = browser.find_element(By.CSS_SELECTOR, ".r-19yznuf > div")
        logIn.click()

        try:
            wait = WebDriverWait(browser, 5)
            cred_error = wait.until(EC.presence_of_element_located((By.XPATH, os.getenv('CREDENTIAL_ERROR_MESSAGE'))))
            print(str(cred_error.text))
            "hello" + 123
        except Exception as e:
            print("Password Exception type:", type(e).__name__)
            if type(e).__name__ == "TypeError":
                raise WrongPasswordException(str(cred_error.text))
            else:
                pass

        try:
            sus = browser.find_element(By.XPATH, "//span[contains(@class, 'css-1jxf684') and contains(@class, 'r-bcqeeo') and contains(@class, 'r-1ttztb7') and contains(@class, 'r-qvutc0') and contains(@class, 'r-poiln3') and text()='Suspicious login prevented']")
            "hello" + 123
        except Exception as e:
            print("Suspicious login Exception type:", type(e).__name__)
            if type(e).__name__ == "TypeError":
                raise SuspiciousLoginException(str(sus.text))
            else:
                pass

        try:
            wait = WebDriverWait(browser, 10)
            wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div'
            )))
            return True
            
        except Exception as e:
            raise LoginFailedException(str(e))
            
    except Exception as e:
        if not isinstance(e, LoginException):
            raise LoginFailedException(str(e))
        raise e
    

def logout(browser):
    browser.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div[4]/div",
    ).click()
    browser.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/a[2]/div[1]/div/span",
    ).click()
    browser.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span/span",
    ).click()
    time.sleep(5)

