import os
from get_chrome_driver import GetChromeDriver
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
from datetime import datetime, timedelta
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from backup import backup
from class_Tweet import (
    ID,
    Comment,
    PostTopic,
    Reactions,
    Response,
    Source,
    Topic,
    Tweet,
)
from cookies import load_cookies, save_cookies
from get_source import responseOb
from login import login, logout
from parse_number import parse_number_with_suffix, timedelta_to_str
from post_Link import id_and_get_post_link, search_and_get_post_link
from timechange import timeChange
from app_configs import SIMS_API_BASEURL, SIMS_API_DATA_CREATE_ENDPOINT
from checksum import generate_checksum

# keyWord = input("Enter Key for Search:")


def clickshowmore():
    # try:
    #     browser.find_element(
    #         By.XPATH,
    #         "//div[@class='css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-q4m81j r-a023e6 r-rjixqe r-16dba41']/span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']",
    #     ).click()
    #     browser.execute_script("window.scrollTo(0,window.scrollY+2000)")
    #     time.sleep(1)
    #     return
    # except:
    #     None
    try:
        browser.find_element(
            By.XPATH,
            "//button//span[contains(text(), 'Show')]",
        ).click()
        browser.execute_script("window.scrollTo(0,window.scrollY+800)")
        # print("Click Show")
        time.sleep(1)
        return
    except:
        None

    # try:
    #     browser.find_element(
    #         By.XPATH,
    #         "//*[contains(text(), 'Show more replies')]",
    #     ).click()
    #     browser.execute_script("window.scrollTo(0,window.scrollY+2000)")
    #     print("Click Show More Replies")
    #     time.sleep(1)
    #     return

    # except:
    #     None
    # time.sleep(2)


def post_scrap(post_url, sourceobj: Source, browser):
    current_datetime = datetime.now()
    featured_Images = []
    browser.get(post_url)
    time.sleep(3)
    # browser.execute_script("window.scrollTo(0,window.scrollY+6000)")
    # time.sleep(5)
    try:
        posted_at = browser.find_element(By.XPATH, "//time").get_attribute("datetime")
        # print("Posted At try:", posted_at)

        if days_ago > datetime.strptime(timeChange(posted_at), "%Y-%m-%d %H:%M:%S"):
            time.sleep(10)
            return
    except:
        posted_at = ""
        # print("Posted At except:", posted_at)
    try:
        post_source = browser.find_element(
            By.XPATH, "//*/div[1]/div/a/div/div[1]/span/span"
        ).text
        # print("Source try:", post_source)
    except:
        source = None
        # print("Source except:", post_source)
    try:
        posted_text = browser.find_element(
            By.XPATH,
            "//div[@class='css-175oi2r']/div[@class='css-175oi2r r-1s2bzr4']/div",
        ).text
        # print("Posted Text try:", posted_text)
    except:
        posted_text = ""
        # print("Posted Text except:", posted_text)

    post_url_web = None

    Total = None
    Sad = None
    try:
        # Love_str = browser.find_element(
        #     By.XPATH,
        #     "//div[@data-testid='cellInnerDiv'][1]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][3]//span[@class='css-1qaijid r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-s1qlax']/span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']",
        # ).text
        Love_str = browser.find_element(
            By.XPATH,
            "//div[@data-testid='cellInnerDiv'][1]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][3]//span[@class='css-1jxf684 r-1ttztb7 r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-n7gxbd']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']",
        ).text
        Love = int(Love_str)
        # print("Love try:", Love)
    except:
        Love = None
        # print("Love except:", Love)
    Wow = None
    Like = None
    Haha = None
    Angry = None
    Care = None

    try:
        # total_comments = browser.find_element(
        #     By.XPATH,
        #     "//div[@data-testid='cellInnerDiv'][1]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][1]//span[@class='css-1qaijid r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-s1qlax']/span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']",
        # ).text
        total_comments = browser.find_element(
            By.XPATH,
            "//div[@data-testid='cellInnerDiv'][1]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][1]//span[@class='css-1jxf684 r-1ttztb7 r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-n7gxbd']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']",
        ).text
        # print("Total Comments try:", total_comments)

    except:
        total_comments = "0"
        print("Total Comments except:", total_comments)
    try:
        # total_shares_text = browser.find_element(
        #     By.XPATH,
        #     "//div[@data-testid='cellInnerDiv'][1]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][2]//span[@class='css-1qaijid r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-s1qlax']/span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']",
        # ).text

        total_shares_text = browser.find_element(
            By.XPATH,
            "//div[@data-testid='cellInnerDiv'][1]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][2]//span[@class='css-1jxf684 r-1ttztb7 r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-n7gxbd']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']",
        ).text

        total_shares = int(total_shares_text)
        # print("Total Shares try:", total_shares)
    except:
        total_shares = None
        print("Total Shares except:", total_shares)

    total_comments = parse_number_with_suffix(total_comments)
    comment_link = []

    try:
        # time.sleep(10)
        url_screenshot = browser.find_element(
            By.XPATH,
            "(//div[@data-testid='cellInnerDiv'][1]//article//div//img[@draggable='true'])[2]",
        ).get_attribute("src")
        # print("URL SS try:", url_screenshot)
    except Exception as e:
        url_screenshot = None
        print("URL SS Error:", e)
        # print("URL SS except:", url_screenshot)

    try:
        featured_Image = browser.find_elements(
            By.XPATH,
            "//div[@data-testid='cellInnerDiv'][1]//article//div//img[@draggable='true']",
        )
        featured_Image = [image.get_attribute("src") for image in featured_Image]
        # print(featured_Image)
        if len(featured_Image) > 2:
            featured_Images += featured_Image[2:]
        # print("URL SS try:", featured_Images)
    except Exception as e:
        featured_Images = None
        print("URL SS Error:", e)
        # print("URL SS except:", featured_Images)

    try:
        #     comment = browser.find_elements(
        #     By.XPATH,
        #     "//div[@class='css-175oi2r']/div/span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']",
        # )
        comment = browser.find_elements(By.XPATH, "//*/div[2]/div/div[3]/a")

        for n in comment:
            comment_link.append(n.get_attribute("href"))
    except:
        comment = []

    for x in range(0, int(total_comments), 4):
        clickshowmore()
        try:
            browser.execute_script("window.scrollTo(0,window.scrollY+400)")
            # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        except Exception as e:
            print("Exception:Couldn't Scroll!:", e)
            browser.execute_script("window.scrollTo(0,window.scrollY-400)")
            # time.sleep(2)
        try:
            #     comment = browser.find_elements(
            #     By.XPATH,
            #     "//div[@class='css-175oi2r']/div/span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']",
            # )
            comment = browser.find_elements(By.XPATH, "//*/div[2]/div/div[3]/a")

            for n in comment:
                comment_link.append(n.get_attribute("href"))
        except:
            comment = []
        print(len(comment_link))

    comments = []

    comment_link = list(dict.fromkeys(comment_link))
    print(len(comment_link))
    # logout(browser)
    # if len(comment_link) > 20:
    #     comment_link = comment_link[:20]
    try:
        for cm in comment_link:
            if "x.com" not in cm:
                continue
            # print(comments)
            try:
                browser.get(cm)
                time.sleep(1)
            except:
                comment_text = "Comment Unavailable"

            try:
                user_name = browser.find_element(
                    By.XPATH,
                    "//div[@data-testid='cellInnerDiv'][2]//span[@class='css-1jxf684 r-dnmrzs r-1udh08x r-1udbk01 r-3s2u2q r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']",
                ).text
                # print("User Name try:", user_name)
            except:
                print("User Not Found!.")
                continue
                # user_name = "Not Found"

            try:
                user_pro_pic = browser.find_element(
                    By.XPATH,
                    "//div[@data-testid='cellInnerDiv'][2]//div[@class='css-175oi2r r-18u37iz']//img",
                ).get_attribute("src")
                user_pro_pic = user_pro_pic.replace("_bigger", "")
            except:
                user_pro_pic = None

            try:

                user_profile_url = browser.find_element(
                    By.XPATH,
                    "(//*/a[@class='css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21'])[3]",
                ).get_attribute("href")
                # user_pro_pic = user_profile_url + "/photo"
            except:
                user_profile_url = "Not  Found"
                user_pro_pic = None

            try:
                comment_text = browser.find_element(
                    By.XPATH, "//*/div[@class='css-175oi2r r-1s2bzr4']/div"
                ).text
                # print("Comment Text try:", comment_text)
            except:
                comment_text = ""
                print("Comment Text except:", comment_text)

            try:
                comment_time = timeChange(
                    browser.find_element(By.XPATH, "(//time)[2]").get_attribute(
                        "datetime"
                    )
                )
            except:
                comment_time = None

            try:
                no_com_rep = browser.find_element(
                    By.XPATH,
                    "//div[@data-testid='cellInnerDiv'][2]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][1]//span[@class='css-1jxf684 r-1ttztb7 r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-n7gxbd']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']",
                ).text

                # print("Reply Try: ", no_com_rep)
            except:
                no_com_rep = 0
                print("Reply Except: ", no_com_rep)

            comments_replies_list = []

            print("Reply:", no_com_rep)
            if int(no_com_rep) > 0:
                clickshowmore()
                rep_list = browser.find_elements(
                    By.XPATH,
                    "//div[@class='css-175oi2r' and @data-testid='cellInnerDiv']",
                )

                # print(len(rep_list))

                try:
                    clickshowmore()
                    time.sleep(1)
                    for repl in range(len(rep_list) - 3):
                        # print(repl)
                        ixp = (
                            "//div[@class='css-175oi2r' and @data-testid='cellInnerDiv']"
                            + "["
                            + str(repl + 4)
                            + "]"
                        )
                        # print(ixp)
                        try:
                            rep_user_name = browser.find_element(
                                By.XPATH,
                                ixp
                                + "//span[contains(@class, 'css-1jxf684') and contains(@class, 'r-dnmrzs') and contains(@class, 'r-1udh08x') and contains(@class, 'r-1udbk01') and contains(@class, 'r-3s2u2q') and contains(@class, 'r-bcqeeo') and contains(@class, 'r-1ttztb7') and contains(@class, 'r-qvutc0') and contains(@class, 'r-poiln3')]/span[contains(@class, 'css-1jxf684') and contains(@class, 'r-bcqeeo') and contains(@class, 'r-1ttztb7') and contains(@class, 'r-qvutc0') and contains(@class, 'r-poiln3')]",
                            ).text
                            # print(rep_user_name)
                        except Exception as err:
                            continue
                            rep_user_name = "Not Found"
                            print(err)

                        try:
                            rep_user_pro_pic = browser.find_element(
                                By.XPATH,
                                ixp + "//div[@class='css-175oi2r r-18u37iz']//img",
                            ).get_attribute("src")
                            rep_user_pro_pic = user_pro_pic.replace("_bigger", "")
                        except Exception as err:
                            rep_user_pro_pic = None
                            print(err)

                        try:

                            rep_user_profile_url = browser.find_element(
                                By.XPATH,
                                ixp
                                + "//a[@class='css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21']",
                            ).get_attribute("href")
                            # user_pro_pic = user_profile_url + "/photo"
                        except Exception as err:
                            rep_user_profile_url = "Not  Found"
                            print(err)

                        try:
                            rep_comment_text = browser.find_element(
                                By.XPATH,
                                ixp
                                + "//div[contains(@class, 'css-146c3p1') and contains(@class, 'r-8akbws') and contains(@class, 'r-krxsd3') and contains(@class, 'r-dnmrzs') and contains(@class, 'r-1udh08x') and contains(@class, 'r-bcqeeo') and contains(@class, 'r-1ttztb7') and contains(@class, 'r-qvutc0') and contains(@class, 'r-37j5jr') and contains(@class, 'r-a023e6') and contains(@class, 'r-rjixqe') and contains(@class, 'r-16dba41') and contains(@class, 'r-bnwqim')]",
                            ).text
                        except Exception as err:
                            rep_comment_text = ""
                            print('rep_comment_text_Error:',err)

                        try:
                            rep_comment_time = timeChange(
                                browser.find_element(
                                    By.XPATH, ixp + "//time"
                                ).get_attribute("datetime")
                            )
                        except Exception as err:
                            rep_comment_time = None
                            print(err)

                        comments_replies_list.append(
                            Comment(
                                rep_user_pro_pic,
                                rep_comment_time,
                                rep_user_name,
                                rep_user_profile_url,
                                rep_comment_text,
                                [],
                            ).__dict__
                        )
                except Exception as err:
                    print(err)
                    None

            commnt = Comment(
                user_pro_pic,
                comment_time,
                user_name,
                user_profile_url,
                comment_text,
                comments_replies_list,
            )
            # print(commnt)
            comments.append(commnt)
            # browser.back()
            # time.sleep(1)
            print(len(comments))
            # print(comments)
    except Exception as e:
        print("Comment link exception:", e)
    # login(browser)

    # browser.back()

    d = ""

    id = ID(d)
    # posted_at = PostedAt(posted_at)
    posted_at = timeChange(posted_at)

    label = ""
    score = ""
    topic = Topic(label, score)

    status = ""
    post_topic = PostTopic(status, topic)

    reactions = Reactions(Love, Sad, Love, Wow, Like, Haha, Angry, Care)

    return Tweet(
        # id,
        type = sourceobj.type,
        source =post_source,
        post_url = post_url,
        post_title = None,
        post_url_web = post_url_web,
        url_screenshot = url_screenshot,
        posted_at =posted_at,
        post_text = posted_text,
        post_topic =post_topic,
        comments = comments,
        reactions = reactions,
        featured_image = featured_Images,
        total_comments = total_comments,
        percent_comments = None,
        total_shares = total_shares,
        vitality_score = None,
        checksum = generate_checksum(post_url),
        source_img=url_screenshot,
        device=source_obj.data.device,
        source_id=sourceobj.id,
        scraped_at=current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        scraping_duration=timedelta_to_str(datetime.now() - current_datetime),
    )


def read_source():
    file_path = "source.json"
    data = {}
    # Load the JSON file
    try:
        with open(file_path, "r") as file:
            data = json.load(file)  # Load the file content as a dictionary
            print("JSON content as a dictionary:")
            # print(data)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    return data


# tlink = read_source()


# print(source_obj)
# print(type(tlink),"\n",len(tlink))
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
option.add_argument("--disable-infobars")
service = Service(executable_path=chrome_file_path)
print(chrome_file_path)
url = "https://x.com"

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
# Let's the user see and also load the element
time.sleep(5)
# --------------search------------
time.sleep(5)
while True:
    scroll = 0
    timestamp_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    source_obj = responseOb()
    if source_obj is None:
        print(f"Due to Get Data From Source Falied! , the script wait {datetime.now()}")
        time.sleep(600)
        continue
    if not source_obj.data:
        print(f"Due to Got Data From Source Empty!, or missmatch , the script wait {datetime.now()}")
        time.sleep(600)
        continue

    days_ago = datetime.fromisoformat(source_obj.data.scraping_duration)
    # days_ago = datetime.now() - timedelta(days=3)
    print("Days Ago: ",days_ago)

    try:
        browser.refresh()   #refresh the page according to if it will wait a lot of time or need to interact with different window before scrapping
    except Exception as e:
        print("Couldn't refress: ",e)

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
                source_obj.data.fb_user.username,
                source_obj.data.fb_user.password,
            )
            browser.find_element(
                By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div'
            )
            print("Logged In Successfull >>>>>>")
        except Exception as e:
            print("Error Log In: ", e)
            print("Log In Failed! Manually Log In ....")
            input("Press Enter To Continue......")
        finally:
            save_cookies(browser)

    for x_source in source_obj.data.sources:
        print(x_source.url)
        xlink = x_source.url
        # print(tlink)

        if "http" in xlink:
            if "status" in xlink:
                link_post = [xlink]
            else:
                link_post = id_and_get_post_link(browser, xlink, days_ago, scroll)
            # print("Link")
            # continue
        else:
            link_post = search_and_get_post_link(browser, xlink, days_ago, scroll)
            # print("Search")
            # continue
        # link_post = search_and_get_post_link(browser, xlink)
        # link_post = id_and_get_post_link(browser, xlink)

        json_list = []
        # link_post = link_post[:1]
        for post_url in link_post:
            if "x.com" not in post_url:
                continue
            try:
                try:
                    post_json = post_scrap(post_url, x_source, browser)
                    if post_json is None:
                        print("The post is Older!")
                        continue
                    print("----------", type(post_json), "---------------")
                    try:
                        json_data = json.dumps(post_json.__dict__)
                        json_list.append(post_json)
                    except Exception as e:
                        if post_json is None:
                            print("The post is Older!")
                        print("Skipped Post Scrapping: ", e)
                        continue

                    print("----------", type(json_data), "---------------")

                    res = requests.post(
                        f"{SIMS_API_BASEURL}{SIMS_API_DATA_CREATE_ENDPOINT}", json_data
                    )
                    print(res.status_code)
                    if res.status_code == 200:
                        print(res)
                        print("---------------success")
                    else:
                        print("---------------Post Fail")
                    # print(json_list)
                except Exception as e:
                    print(e)
                    print("Couldn't Scrap Post!")
                    continue
                
                try:
                    dict_list = [obj.__dict__ for obj in json_list]
                    # print(dict_list)
                except:
                    print("Couldn't Make Dict List!")

                # Convert list of dictionaries to JSON
                json_data = json.dumps(dict_list, indent=4, ensure_ascii=False)
                with open(
                    "tweet.json", "w", encoding="utf-8", errors="ignore"
                ) as json_file:
                    json_file.write(json_data)
                

            except:
                continue

        
        try:
            dict_list = [obj.__dict__ for obj in json_list]
        except:
            continue
        # Convert list of dictionaries to JSON
        json_data = json.dumps(
            dict_list, indent=4, ensure_ascii=False
        )  # Using indent for pretty printing

        # print(json_data)

        with open(
            xlink.split("/")[-1] + ".json", "w", encoding="utf-8", errors="ignore"
        ) as json_file:
            json_file.write(json_data)

        # try:
        #     with open(str(tlink.index(xlink))+".json", "w", encoding="utf-8", errors="ignore") as json_file:
        #         json_file.write(json_data)
        # except:
        #     None

        backup(xlink.split("/")[-1])

        with open("tweet.json", "r", encoding="utf-8", errors="ignore") as file:
            # Load the JSON data
            data = json.load(file)
        
    # time.sleep(86400)
    # Path to the JSON file
    # file_path = "source.json"

    # # Write dictionary to JSON file
    # try:
    #     with open(file_path, "w") as file:
    #         json.dump(tlink, file, indent=4)  # Use indent for pretty formatting
    #     print(f"Dictionary has been written to {file_path}.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
