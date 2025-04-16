import time
from selenium.webdriver.common.by import By

def login(browser,username,password):
    login = browser.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")

    # using the click function which is similar to a click in the mouse.
    login.click()

    print("Login in Twitter")

    time.sleep(5)

    user = browser.find_element(By.CSS_SELECTOR, ".r-30o5oe")

    # Enter User Name
    user_name = username
    user.send_keys(user_name)

    next = browser.find_element(By.XPATH, "//span[text()='Next']")
    # input('ok')
    next.click()

    time.sleep(5)
    # input('ok')
    passw = browser.find_element(By.CSS_SELECTOR, ".r-homxoj")
    # input('ok')
    user_pass = password
    passw.send_keys(user_pass)
    time.sleep(5)
    # input('ok')
    logIn = browser.find_element(By.CSS_SELECTOR, ".r-19yznuf > div")
    # input('ok')
    logIn.click()
    # input('ok')
    print("Login Successful")

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

