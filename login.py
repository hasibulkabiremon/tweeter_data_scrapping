import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(browser, user_name, user_pass):
    login = browser.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")

    # using the click function which is similar to a click in the mouse.
    login.click()

    print("Login in Twitter")

    time.sleep(5)

    user = browser.find_element(By.CSS_SELECTOR, ".r-30o5oe")

    # Enter User Name
    user.send_keys(user_name)

    next = browser.find_element(By.XPATH, "//span[text()='Next']")
    # input('ok')
    next.click()

    try:
        wait = WebDriverWait(browser, 5)
        cred_error = wait.until(EC.presence_of_element_located((By.XPATH, os.getenv('CREDENTIAL_ERROR_MESSAGE'))))
        return "Login with username Failed: " + str(cred_error.text)
    except Exception as e:
        pass

    time.sleep(5)
    # input('ok')
    passw = browser.find_element(By.CSS_SELECTOR, ".r-homxoj")
    # input('ok')
    passw.send_keys(user_pass)
    time.sleep(5)
    # input('ok')
    logIn = browser.find_element(By.CSS_SELECTOR, ".r-19yznuf > div")
    # input('ok')
    logIn.click()
    # input('ok')

    try:
        wait = WebDriverWait(browser, 5)
        cred_error = wait.until(EC.presence_of_element_located((By.XPATH, os.getenv('CREDENTIAL_ERROR_MESSAGE'))))
        return "Login with username and password Failed: " + str(cred_error.text)
    except Exception as e:
        pass

    try:
        sus = browser.find_element(By.XPATH, "//span[contains(@class, 'css-1jxf684') and contains(@class, 'r-bcqeeo') and contains(@class, 'r-1ttztb7') and contains(@class, 'r-qvutc0') and contains(@class, 'r-poiln3') and text()='Suspicious login prevented']")
        return "Login with username and password Failed: " + str(sus.text)
    except Exception as e:
        pass

    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div'
        )))
        return "Log in with credentials Successful"
    except Exception as e:
        return "Log in with credentials Failed: " + str(e)
    

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

