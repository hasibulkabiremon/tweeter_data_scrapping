from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from timechange import timeChange

def search_and_get_post_link(browser, topic,days_ago,loop_range=1):
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
        By.XPATH, "//div[@class='css-175oi2r r-18u37iz r-1q142lx']/a"
    )
    link_post += [l.get_attribute("href") for l in tw_post]

    for l in tw_post:
        try:
            time_element = timeChange(l.find_element(By.XPATH, ".//time").get_attribute("datetime")) #Post Time
        except Exception as e:
            print(e)
        if datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago:
            link_post.append(l.get_attribute("href"))
            print("Link Appended.")
        else:
            print(datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago)


    # for l in tw_post:
    #     tt = l.find_element(By.XPATH, "//time").text
    #     print(tt)
    #     if tt[-1] == "h" or tt[-1] == "m":
    #         print("append", tt[-1])
    #         link_post.append(l.get_attribute("href"))
    #     else:
    #         print(tt[-1])
    #         None

    while loop_range < 10:
        browser.execute_script("window.scrollTo(0,window.scrollY+4000)")
        time.sleep(5)
        tw_post = browser.find_elements(
            By.XPATH, "//div[@class='css-175oi2r r-18u37iz r-1q142lx']/a"
        )
        for l in tw_post:
            time_element = timeChange(l.find_element(By.XPATH, ".//time").get_attribute("datetime"))
            if datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago:
                link_post.append(l.get_attribute("href"))
                print("Link Appended.")
            else:
                print(datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago)
                loop_range+=1

    link_post = list(dict.fromkeys(link_post))

    print(len(link_post))
    [print(l) for l in link_post]
    # print("Key:")
    return link_post


def id_and_get_post_link(browser, link, days_ago, loop_range=1):
    link_post = []
    browser.get(link)
    time.sleep(5)

    tw_post = browser.find_elements(
        By.XPATH, "//div[@class='css-175oi2r r-18u37iz r-1q142lx']/a"
    )
    # link_post += [l.get_attribute("href") for l in tw_post if datetime.strptime(timeChange(l.find_element(By.XPATH, ".//time").get_attribute("datetime")),"%Y-%m-%d %H:%M:%S") > days_ago]

    for l in tw_post:
        try:
            time_element = timeChange(l.find_element(By.XPATH, ".//time").get_attribute("datetime")) #Post Time
        except Exception as e:
            print(e)
        if datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago:
            link_post.append(l.get_attribute("href"))
            print("Link Appended.")
        else:
            print(datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago)


    while loop_range < 10:
        browser.execute_script("window.scrollTo(0,window.scrollY+2000)")
        time.sleep(2)
        tw_post = browser.find_elements(
            By.XPATH, "//div[@class='css-175oi2r r-18u37iz r-1q142lx']/a"
        )
        # link_post += [l.get_attribute("href") for l in tw_post]

        for l in tw_post:
            try:
                time_element = timeChange(l.find_element(By.XPATH, ".//time").get_attribute("datetime"))
            except Exception as e:
                print(e)
                continue
            if datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago:
                link_post.append(l.get_attribute("href"))
                print("Link Appended.")
            else:
                print(datetime.strptime(time_element,"%Y-%m-%d %H:%M:%S") > days_ago)
                loop_range +=1

        # out_break = False
        # for l in tw_post:
        #     tt = l.find_element(By.XPATH, "//time").text
        #     print(tt)
        #     if tt[-1] == "h" or tt[-1] == "m":
        #         print("append", tt[-1])
        #         link_post.append(l.get_attribute("href"))
        #     else:
        #         print(tt[-1])
        #         out_break = True
        # break
        # if out_break:
        # break

    link_post = list(dict.fromkeys(link_post))

    print(len(link_post))
    [print(l) for l in link_post]
    # input("ID:")
    return link_post

