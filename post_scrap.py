import time
from class_Tweet import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from parse_number import parse_number_with_suffix
from timechange import timeChange

def post_scrap(post_url, browser):
    # browser.get(post_url)
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

