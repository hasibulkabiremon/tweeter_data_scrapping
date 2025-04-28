# Import necessary libraries
import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from dotenv import load_dotenv
# Import custom modules
from class_Tweet import ID, Comment, PostTopic, Reactions, Topic, Tweet
from login import login, logout
from parse_number import parse_number_with_suffix
from timechange import timeChange
load_dotenv()

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


def click_show_more(browser):
    """Click the 'Show more' button if available and scroll down."""
    
    try:
        browser.find_element(By.XPATH, "//button//span[contains(text(), 'Show')]").click()
        print("Clicked 'Show more'")
    
    except Exception as e:
        # print(f"Show more button not found: {e}")
        pass
    

def post_scrap(post_url, browser):
    """Scrape post details from the given URL using the provided browser instance."""
    featured_images = []
    browser.get(post_url)
    time.sleep(3)

    # Extract post details
    try:
        posted_at = browser.find_element(By.XPATH, "//time").get_attribute("datetime")
        if not posted_at:
            print("No post date found, skipping post.")
            return None
    except Exception as e:
        print(f"Error retrieving post date: {e}")
        return None

    try:
        source = browser.find_element(By.XPATH, "//*/div[1]/div/a/div/div[1]/span/span").text
    except Exception as e:
        print(f"Error retrieving source: {e}")
        source = None

    try:
        posted_text = browser.find_element(By.XPATH, "//div[@class='css-175oi2r']/div[@class='css-175oi2r r-1s2bzr4']/div").text
    except Exception as e:
        print(f"Error retrieving posted text: {e}")
        posted_text = ""

    # Extract reactions
    try:
        love_str = browser.find_element(By.XPATH, "//div[@data-testid='cellInnerDiv'][1]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][3]//span[@class='css-1jxf684 r-1ttztb7 r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-n7gxbd']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']").text
        love = parse_number_with_suffix(love_str)
        # print('Love:',love)
    except Exception as e:
        print(f"Error retrieving love reactions: {e}")
        love = None
    try:
        total_shares = browser.find_element(By.XPATH, os.getenv('TOTAL_SHARES_PATH')).text
        total_shares = parse_number_with_suffix(total_shares)
    except Exception as e:
        print(f"Error retrieving total shares:")
        total_shares = None
    # Extract comments
    try:
        total_comments = browser.find_element(By.XPATH, "//div[@data-testid='cellInnerDiv'][1]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][1]//span[@class='css-1jxf684 r-1ttztb7 r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-n7gxbd']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']").text
    except Exception as e:
        print(f"Error retrieving total comments: {e}")
        total_comments = "0"

    total_comments = parse_number_with_suffix(total_comments)
    comment_links = []

    # Extract images
    try:
        featured_image_elements = browser.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv'][1]//article//div//img[@draggable='true']")
        featured_images = [image.get_attribute("src") for image in featured_image_elements]
    except Exception as e:
        print(f"Error retrieving images: {e}")

    '''# Extract comments
    print('Extract comments->>>>>')
    try:
        comments = extract_comments(browser, total_comments)
    except Exception as e:
        print(f"Error extracting comments: {e}")
        comments = []
    print('Comments:', comments)'''

    
    # print('comment_elements:',len(comment_elements))
    comments_for_scrap = []
    comments = extract_comments(browser,comments_for_scrap,total_comments)
    # Create Tweet object
    reactions = Reactions(Total=love, Sad=None, Love=love, Wow=None, Like=None, Haha=None, Angry=None, Care=None)
    try:
        post_topic = PostTopic(status=None, topic=Topic(label=None, score=None))
        tweet = Tweet(
            type=None,
            source=source,
            post_url=post_url,
            post_title=None,
            post_url_web=None,
            url_screenshot=None,
            posted_at=timeChange(posted_at),
            post_text=posted_text,
            post_topic=post_topic,
            comments=comments,
            reactions=reactions,
            featured_image=featured_images,
            total_comments=total_comments,
            percent_comments=None,
            total_shares=total_shares,
            vitality_score=None,
            checksum=None
        )
    except Exception as e:
        print(f"Error creating Tweet object: {e}")
        tweet = None
    
    # Print details of the tweet as JSON
    
    # print('Tweet Details:', json.dumps(tweet.__dict__, indent=4))
    
    return tweet


def extract_comments(browser,comments_for_scrap,total_comments):

    for _ in range(0, int(total_comments), 30):
        browser.implicitly_wait(0)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        click_show_more(browser)
        comment_elements = browser.find_elements(By.XPATH, os.getenv('COMMENT_PATH'))
        
        
        for comment in comment_elements:
            try:
                user_name = comment.find_element(By.XPATH, os.getenv('USER_NAME_PATH')).text
                # print('user_name:',user_name)
                user_pro_pic = comment.find_element(By.XPATH, os.getenv('USER_PRO_PIC_PATH')).get_attribute("src").replace("_bigger", "")
                # print('user_pro_pic:',user_pro_pic)
                user_profile_url = comment.find_element(By.XPATH, os.getenv('USER_PROFILE_URL_PATH')).get_attribute("href")
                # print('user_profile_url',user_profile_url)

                try:
                    comment_text = comment.find_element(By.XPATH, os.getenv('COMMENT_TEXT_PATH')).text
                    # print('comment_text',comment_text)
                except Exception as e:
                    print(f"Error retrieving comment text:")
                    comment_text = ""
                comment_time = timeChange(comment.find_element(By.XPATH, os.getenv('COMMENT_TIME_PATH')).get_attribute("datetime"))
                # print('comment_time',comment_time)
                # try:
                #     no_com_rep = comment.find_element(By.XPATH, os.getenv('NO_COM_REP_PATH')).text
                #     print('no_com_rep',no_com_rep)
                # except Exception as e:
                #     print(f"Error retrieving comment replies: {e}")
                #     no_com_rep = 0
                comments_replies_list = []
                # print('comments_replies_list',comments_replies_list)
                comments_for_scrap.append(Comment(user_pro_pic, comment_time, user_name, user_profile_url, comment_text, comments_replies_list))
                # print('Comments',comments)
            except Exception as e:
                print(f"Error processing comment link: {e}")
    browser.implicitly_wait(5)
    unique_comments = []
    seen = set()
    for comment in comments_for_scrap:
        comment_data = (comment.user_pro_pic, comment.comment_time, comment.user_name, comment.user_profile_url, comment.comment_text)
        if comment_data not in seen:
            unique_comments.append(comment)
            seen.add(comment_data)
    return unique_comments

    """Extract comments from the post."""
    '''comment_links = []
    comments = []

    for _ in range(0, int(total_comments), 4):
        click_show_more(browser)
        try:
            browser.execute_script("window.scrollTo(0,window.scrollY+400)")
            time.sleep(1)
        except Exception as e:
            print(f"Error scrolling: {e}")

        try:
            comment_elements = browser.find_elements(By.XPATH, "//*/div[2]/div/div[3]/a")
            for element in comment_elements:
                comment_links.append(element.get_attribute("href"))
        except Exception as e:
            print(f"Error retrieving comment links: {e}")


    comment_links = list(dict.fromkeys(comment_links))  # Remove duplicates
    for link in comment_links[:2]:
        if "x.com" not in link:
            continue
        try:
            browser.get(link)
            time.sleep(1)
            user_name = browser.find_element(By.XPATH, "//div[@data-testid='cellInnerDiv'][2]//span[@class='css-1jxf684 r-dnmrzs r-1udh08x r-1udbk01 r-3s2u2q r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']").text
            print('user_name',user_name)
            user_pro_pic = browser.find_element(By.XPATH, "//div[@data-testid='cellInnerDiv'][2]//div[@class='css-175oi2r r-18u37iz']//img").get_attribute("src").replace("_bigger", "")
            print('user_pro_pic',user_pro_pic)
            user_profile_url = browser.find_element(By.XPATH, "(//*/a[@class='css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21'])[3]").get_attribute("href")
            print('user_profile_url',user_profile_url)
            try:
                comment_text = browser.find_element(By.XPATH, "//*/div[@class='css-175oi2r r-1s2bzr4']/div").text
                print('comment_text',comment_text)
            except Exception as e:
                print(f"Error retrieving comment text: {e}")
                comment_text = ""
            comment_time = timeChange(browser.find_element(By.XPATH, "(//time)[2]").get_attribute("datetime"))
            print('comment_time',comment_time)
            try:
                no_com_rep = browser.find_element(By.XPATH, "//div[@data-testid='cellInnerDiv'][2]//div[@class='css-175oi2r r-18u37iz r-1h0z5md r-13awgt0'][1]//span[@class='css-1jxf684 r-1ttztb7 r-qvutc0 r-poiln3 r-n6v787 r-1cwl3u0 r-1k6nrdp r-n7gxbd']/span[@class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']").text
                print('no_com_rep',no_com_rep)
            except Exception as e:
                print(f"Error retrieving comment replies: {e}")
                no_com_rep = 0
            comments_replies_list = []
            print('comments_replies_list',comments_replies_list)
            comments.append(Comment(user_pro_pic, comment_time, user_name, user_profile_url, comment_text, comments_replies_list))
            print('Comments',comments)
        except Exception as e:
            print(f"Error processing comment link {link}: {e}")
    return comments'''


def extract_replies(browser, no_com_rep):
    """Extract replies to a comment."""
    comments_replies_list = []
    if no_com_rep > 0:
        click_show_more(browser)
        rep_list = browser.find_elements(By.XPATH, "//div[@class='css-175oi2r' and @data-testid='cellInnerDiv']")

        for repl in range(len(rep_list) - 3):
            ixp = f"//div[@class='css-175oi2r' and @data-testid='cellInnerDiv'][{repl + 4}]"
            try:
                rep_user_name = browser.find_element(By.XPATH, ixp + "//span[contains(@class, 'css-1jxf684') and contains(@class, 'r-dnmrzs') and contains(@class, 'r-1udh08x') and contains(@class, 'r-1udbk01') and contains(@class, 'r-3s2u2q') and contains(@class, 'r-bcqeeo') and contains(@class, 'r-1ttztb7') and contains(@class, 'r-qvutc0') and contains(@class, 'r-poiln3')]/span[contains(@class, 'css-1jxf684') and contains(@class, 'r-bcqeeo') and contains(@class, 'r-1ttztb7') and contains(@class, 'r-qvutc0') and contains(@class, 'r-poiln3')]").text
                rep_user_pro_pic = browser.find_element(By.XPATH, ixp + "//div[@class='css-175oi2r r-18u37iz']//img").get_attribute("src").replace("_bigger", "")
                rep_user_profile_url = browser.find_element(By.XPATH, ixp + "//a[@class='css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21']").get_attribute("href")
                rep_comment_text = browser.find_element(By.XPATH, ixp + "//div[contains(@class, 'css-146c3p1') and contains(@class, 'r-8akbws') and contains(@class, 'r-krxsd3') and contains(@class, 'r-dnmrzs') and contains(@class, 'r-1udh08x') and contains(@class, 'r-bcqeeo') and contains(@class, 'r-1ttztb7') and contains(@class, 'r-qvutc0') and contains(@class, 'r-37j5jr') and contains(@class, 'r-a023e6') and contains(@class, 'r-rjixqe') and contains(@class, 'r-16dba41') and contains(@class, 'r-bnwqim')]").text
                rep_comment_time = timeChange(browser.find_element(By.XPATH, ixp + "//time").get_attribute("datetime"))
                comments_replies_list.append(Comment(rep_user_pro_pic, rep_comment_time, rep_user_name, rep_user_profile_url, rep_comment_text, []))
            except Exception as e:
                print(f"Error processing reply:")

    return comments_replies_list


def read_source(file_path="source.json"):
    """Read and return the content of the source JSON file."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            print("Loaded JSON content.")
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    return {}


def main():
    if not os.path.exists("post_data"):
        os.makedirs("post_data")
    tlink = read_source()
    print(f"Loaded {len(tlink)} links from source.")

    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.implicitly_wait(5)
    browser.get("https://x.com")
    time.sleep(5)



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

    time.sleep(5)

    for xlink in tlink:
        if "x.com" not in xlink:
            continue
        try:
            try:
                scrap_data = post_scrap(xlink, browser)
                # print('1',scrap_data)
            except Exception as e:
                print(f"Error scraping post: {e}")
                print(scrap_data)
                continue
            if scrap_data is None:
                print(f"No data scraped for link {xlink}. Skipping...")
                continue
            # print('2', scrap_data)
            file_name = f"{xlink.split('/')[-3]}_{xlink.split('/')[-1]}"
            # print('4',file_name)
            with open(f"post_data/{file_name}.json", "w", encoding="utf-8", errors="replace") as json_file:
                json_file.write(json.dumps(scrap_data.__dict__, ensure_ascii=False))
            print(f"Scraped and saved post {file_name}")
        except Exception as e:
            print(f"Error processing link {xlink}: {e}")    



if __name__ == "__main__":
    main()