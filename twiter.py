from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
from datetime import datetime
import pytz
import requests
from selenium.webdriver.chrome.options import Options

# keyWord = input("Enter Key for Search:")

loop_range = 10


def backup(xlink):
    with open("backup.json", "r", encoding="utf-8", errors="ignore") as file:
        # Load the JSON data
        dataSave = json.load(file)

    with open(xlink + ".json", "r", encoding="utf-8", errors="ignore") as file:
        # Load the JSON data
        data = json.load(file)

    dataSave += data

    json_data = json.dumps(dataSave, indent=4, ensure_ascii=False)

    with open("backup.json", "w", encoding="utf-8", errors="ignore") as json_file:
        json_file.write(json_data)


def timeChange(t):
    original_timestamp = t

    # Convert to datetime object
    dt_object_utc = datetime.fromisoformat(original_timestamp.replace("Z", "+00:00"))

    # Convert to Bangladeshi time
    bangladesh_timezone = pytz.timezone("Asia/Dhaka")
    dt_object_bangladesh = dt_object_utc.astimezone(bangladesh_timezone)

    # Convert to desired format
    formatted_timestamp = dt_object_bangladesh.strftime("%Y-%m-%d %H:%M:%S")

    print(formatted_timestamp)
    return formatted_timestamp


def parse_number_with_suffix(s):
    suffixes = {"K": 10**3, "M": 10**6, "B": 10**9, "T": 10**12}

    s = s.upper()
    if s[-1] in suffixes:
        return int(float(s[:-1]) * suffixes[s[-1]])
    return int(float(s))


class Tweet:
    def __init__(
        self,
        # _id,
        type,
        source,
        post_url,
        post_title,
        post_url_web,
        url_screenshot,
        posted_at,
        post_text,
        post_topic,
        comments,
        reactions,
        featured_image,
        total_comments,
        percent_comments,
        total_shares,
        vitality_score,
        checksum,
    ):
        # self._id = _id.__dict__
        self.type = type
        self.source = source
        self.post_url = post_url
        self.post_title = post_title
        self.post_url_web = post_url_web
        self.url_screenshot = url_screenshot
        self.posted_at = posted_at
        self.post_text = post_text
        self.post_topic = post_topic.__dict__
        self.comments = []
        for comment in comments:
            if comment is not None:
                self.comments.append(comment.__dict__)
        self.reactions = reactions.__dict__
        self.featured_image = featured_image
        self.total_comments = total_comments
        self.percent_comments = percent_comments
        self.total_shares = total_shares
        self.vitality_score = vitality_score
        self.checksum = checksum


class ID:
    def __init__(self, oid):
        self.oid = oid


class PostedAt:
    def __init__(self, posted_at):
        self.posted_at = posted_at


class Topic:
    def __init__(self, label, score):
        self.label = label
        self.score = score


class PostTopic:
    def __init__(self, status, topic):
        self.status = status
        self.topic = topic.__dict__


class Comment:
    def __init__(
        self,
        user_pro_pic,
        comment_time,
        user_name,
        user_profile_url,
        comment_text,
        comments_replies_list,
    ):
        self.user_pro_pic = user_pro_pic
        self.comment_time = comment_time
        self.user_name = user_name
        self.user_profile_url = user_profile_url
        self.comment_text = comment_text
        self.comment_replies = comments_replies_list


class Reactions:
    def __init__(self, Total, Sad, Love, Wow, Like, Haha, Angry, Care):
        self.Total = Total
        self.Sad = Sad
        self.Love = Love
        self.Wow = Wow
        self.Like = Like
        self.Haha = Haha
        self.Angry = Angry
        self.Care = Care


def login(browser):
    login = browser.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")

    # using the click function which is similar to a click in the mouse.
    login.click()

    print("Login in Twitter")

    time.sleep(5)

    user = browser.find_element(By.CSS_SELECTOR, ".r-30o5oe")

    # Enter User Name
    user_name = input("Enter user Name:")
    user.send_keys(user_name)

    next = browser.find_element(By.XPATH, "//span[text()='Next']")
    # input('ok')
    next.click()

    time.sleep(5)
    # input('ok')
    passw = browser.find_element(By.CSS_SELECTOR, ".r-homxoj")
    # input('ok')
    user_pass = input("Enter user Name:")
    passw.send_keys(user_pass)
    time.sleep(5)
    # input('ok')
    logIn = browser.find_element(By.CSS_SELECTOR, ".r-19yznuf > div")
    # input('ok')
    logIn.click()
    # input('ok')
    print("Login Successful")


def search_and_get_post_link(browser, topic):
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

    # for l in tw_post:
    #     tt = l.find_element(By.XPATH, "//time").text
    #     print(tt)
    #     if tt[-1] == "h" or tt[-1] == "m":
    #         print("append", tt[-1])
    #         link_post.append(l.get_attribute("href"))
    #     else:
    #         print(tt[-1])
    #         None

    for noPost in range(loop_range):
        browser.execute_script("window.scrollTo(0,window.scrollY+4000)")
        time.sleep(5)
        tw_post = browser.find_elements(
            By.XPATH, "//div[@class='css-175oi2r r-18u37iz r-1q142lx']/a"
        )
        link_post += [l.get_attribute("href") for l in tw_post]

        # ot_br = False
        # for l in tw_post:
        #     tt = l.find_element(By.XPATH, "//time").text
        #     print(tt)
        #     if tt[-1] == "h" or tt[-1] == "m":
        #         print("append", tt[-1])
        #         link_post.append(l.get_attribute("href"))
        #     else:
        #         print(tt[-1])
        #         ot_br = True
        # break
        # if ot_br:
        #     break

    link_post = list(dict.fromkeys(link_post))

    print(len(link_post))
    [print(l) for l in link_post]
    # print("Key:")
    return link_post


def id_and_get_post_link(browser, link):
    link_post = []
    browser.get(link)
    time.sleep(5)

    tw_post = browser.find_elements(
        By.XPATH, "//div[@class='css-175oi2r r-18u37iz r-1q142lx']/a"
    )
    link_post += [l.get_attribute("href") for l in tw_post]

    # for l in tw_post:
    #     tt = l.find_element(By.XPATH, "//time").text
    #     print(tt)
    #     if tt[-1] == "h" or tt[-1] == "m":
    #         print("append", tt[-1])
    #         link_post.append(l.get_attribute("href"))
    #     else:
    #         print(tt[-1])
    # break

    for noPost in range(loop_range):
        browser.execute_script("window.scrollTo(0,window.scrollY+2000)")
        time.sleep(2)
        tw_post = browser.find_elements(
            By.XPATH, "//div[@class='css-175oi2r r-18u37iz r-1q142lx']/a"
        )
        link_post += [l.get_attribute("href") for l in tw_post]

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
        print("Click Show")
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


def post_scrap(post_url, browser):
    browser.get(post_url)
    time.sleep(1)
    # browser.execute_script("window.scrollTo(0,window.scrollY+6000)")
    # time.sleep(5)
    try:
        source = browser.find_element(
            By.XPATH, "//*/div[1]/div/a/div/div[1]/span/span"
        ).text
        print("Source try:", source)
    except:
        source = None
        print("Source except:", source)
    try:
        posted_text = browser.find_element(
            By.XPATH,
            "//div[@class='css-175oi2r']/div[@class='css-175oi2r r-1s2bzr4']/div",
        ).text
        print("Posted Text try:", posted_text)
    except:
        posted_text = ""
        print("Posted Text except:", posted_text)

    try:
        posted_at = browser.find_element(By.XPATH, "//time").get_attribute("datetime")
        print("Posted At try:", posted_at)
    except:
        posted_at = ""
        print("Posted At except:", posted_at)

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
        print("Love try:", Love)
    except:
        Love = None
        print("Love except:", Love)
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
        print("Total Comments try:", total_comments)

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
        print("Total Shares try:", total_shares)
    except:
        total_shares = None
        print("Total Shares except:", total_shares)

    total_comments = parse_number_with_suffix(total_comments)
    comment_link = []

    try:
        # time.sleep(10)
        url_screenshot = browser.find_element(
            By.XPATH,
            "//div[@data-testid='cellInnerDiv'][1]//div[@aria-label]//img",
        ).get_attribute("src")
        print("URL SS try:", url_screenshot)
    except Exception as e:
        url_screenshot = None
        print("URL SS Error:",e)
        print("URL SS except:", url_screenshot)
    

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
            print("Exception:Couldn't Scroll!:",e)
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
            # print(comments)
            try:
                browser.get(cm)
                time.sleep(3)
            except:
                comment_text = "Comment Unavailable"

            try:
                user_name = browser.find_element(
                    By.XPATH,
                    "//div[@data-testid='cellInnerDiv'][2]//span[@class='css-1jxf684 r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']",
                ).text
                print("User Name try:", user_name)
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
                print("Comment Text try:", comment_text)
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
                
                print("Reply Try: ", no_com_rep)
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

                print(len(rep_list))

                
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
                                + "//span[@class='css-1jxf684 r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']",
                            ).text
                            print(rep_user_name)
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
                                + "//div[@class='css-175oi2r']/div[@class='css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim']",
                            ).text
                        except Exception as err:
                            rep_comment_text = ""
                            print(err)

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

    reactions = Reactions(Total, Sad, Love, Wow, Like, Haha, Angry, Care)

    return Tweet(
        # id,
        None,
        source,
        post_url,
        None,
        post_url_web,
        url_screenshot,
        posted_at,
        posted_text,
        post_topic,
        comments,
        reactions,
        None,
        total_comments,
        None,
        total_shares,
        None,
        None,
    )


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


tlink = [
    "https://twitter.com/LionUzzal",
    "https://twitter.com/revolt_71",
    "https://twitter.com/alsbddk75118",
    "https://twitter.com/ForhadTweets",
    "https://twitter.com/rupom",
    "https://twitter.com/PinakiTweetsBD",
    "https://twitter.com/BNPBdMediaCell",
    "https://twitter.com/DrColShahidKhan",
    "https://twitter.com/Chowdhury_Anee",
    "https://twitter.com/Mdjoynal26",
    "https://twitter.com/farhana_rumeen",
    "https://twitter.com/ishraqueBD",
    "https://twitter.com/ABhuttow",
    "https://twitter.com/zahiruddinBNP",
    "https://twitter.com/KamranRajib",
    "https://twitter.com/ronymp70",
    "https://twitter.com/MDABDULOHAB14",
    "https://twitter.com/bbcbangla",
    "https://twitter.com/MonjuAlom1",
    "https://twitter.com/NurulHaqueNur2",
    "বাংলাদেশ ব্যাংকের রিজার্ভ",
    "গুজব",
    "বাংলাদেশ নির্বাচন",
    "বাংলাদেশ কারচুপি",
    "গ্রেফতার বিএনপি",
    "ফ্যাসিবাদী সরকার",
    "আন্দোলন",
    "মামলা",
    "গুম খুন ",
    "রাজাকার ",
    "সন্ত্রাসী বাহিনী",
    "অবৈধ ক্ষমতা",
    "https://twitter.com/MDAMDA359068",
    "আনারুল আজিমের",
    "জেনারেল আজিজ",
    "https://x.com/ABhuttow/status/1701210954254385328",
    "https://x.com/dailystarnews/status/1793954460101919160",
    "https://x.com/HarunIzharBD/status/1793861625134678165",
    "https://x.com/osamaumor/status/1793538455085236414",
    "https://x.com/sorowar1976/status/1793906977535664616",
    "https://x.com/basherkella/status/1793847640506896830",
    "https://x.com/basherkella/status/1730920800470094260",
    "https://x.com/ABhuttow/status/1794506233988223334",
    "রিমাল",
    "রেমাল"
]


browser = webdriver.Chrome()
browser.maximize_window()
browser.implicitly_wait(3)
browser.get("https://x.com")
# Let's the user see and also load the element
time.sleep(5)

login(browser)

# --------------search------------
time.sleep(5)

for xlink in tlink:

    # # id_link = xlink

    # # Creating an instance webdriver
    # browser = webdriver.Chrome()
    # browser.maximize_window()
    # browser.implicitly_wait(10)
    # browser.get("https://www.twitter.com")

    # # Let's the user see and also load the element
    # time.sleep(5)

    # login(browser)

    # # --------------search------------
    # time.sleep(5)
    if "http" in xlink:
        if "status" in xlink:
            link_post = [xlink]
        else:
            link_post = id_and_get_post_link(browser, xlink)
        # print("Link")
        # continue
    else:
        link_post = search_and_get_post_link(browser, xlink)
        # print("Search")
        # continue
    # link_post = search_and_get_post_link(browser, xlink)
    # link_post = id_and_get_post_link(browser, xlink)

    json_list = []
    # link_post = link_post[:1]
    for post_url in link_post:
        try:
            try:
                json_list.append(post_scrap(post_url, browser))
                # print(json_list)
            except:
                print("Couldn't Scrap Post!")
            try:
                dict_list = [obj.__dict__ for obj in json_list]
                # print(dict_list)
            except:
                print("Couldn't Make Dict List!")

            # Convert list of dictionaries to JSON
            json_data = json.dumps(dict_list, indent=4, ensure_ascii=False)

            # print(json_data)
            # Using indent for pretty printing
            # browser.quit()
            # time.sleep(5)
            # browser = webdriver.Chrome()
            # browser.maximize_window()
            # time.sleep(5)
            # browser.get("https://www.twitter.com")
            # browser.implicitly_wait(30)
            # time.sleep(5)
            # login(browser)
            # time.sleep(5)
            # print(json_data)
            with open(
                "tweet.json", "w", encoding="utf-8", errors="ignore"
            ) as json_file:
                json_file.write(json_data)

        except:
            browser = webdriver.Chrome()
            browser.maximize_window()
            time.sleep(5)
            browser.get("https://www.twitter.com")
            browser.implicitly_wait(3)
            time.sleep(5)
            login(browser)
            time.sleep(5)
    dict_list = [obj.__dict__ for obj in json_list]

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

    with open("tweet.json", "r",encoding="utf-8", errors="ignore") as file:
        # Load the JSON data
        data = json.load(file)

    for d in  data:
        # print(type(d))

        json_data = json.dumps(d)

        # print(type(json_data))

        res = requests.post('http://103.113.152.81:8051/create/scraped-data?platform=X',json_data)
        print(res.status_code)
        if res.status_code == 200 :
            print(res)
            print("success")
        else :
            print("Post Fail")
    # try:
    #     browser.quit()
    # except:
    #     None
