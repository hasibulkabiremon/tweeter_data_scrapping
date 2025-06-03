# Import necessary libraries
import asyncio
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

def load_cookies(driver):
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
        show_more_button = browser.find_element(By.XPATH, "//button//span[contains(text(), 'Show')]")
        show_more_button.click()
        print("Clicked 'Show more'")
    except Exception as e:
        # Check if we're inside a try-except block
        pass


def post_scrap(post_url, browser):
    """Scrape post details from the given URL using the provided browser instance."""
    featured_images = []
    browser.get(post_url)
    

    loading_checker(browser)
            
 
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

    visited_reply_links = []
    break_d = 0
    last_height = browser.execute_script("return document.body.scrollHeight")
    print('last_height:',last_height)
    for _ in range(0, int(total_comments)):
        loading_checker(browser)
        browser.implicitly_wait(.5)
        comment_elements = browser.find_elements(By.XPATH, os.getenv('COMMENT_PATH'))
        comment_data_taker(browser ,comments_for_scrap, comment_elements,visited_reply_links)
        click_show_more(browser)
        if 'comment_elements' in locals():
            if len(comment_elements) > 0:
                browser.execute_script("arguments[0].scrollIntoView(true);", comment_elements[-1])

                if last_height == browser.execute_script("return document.body.scrollHeight"):
                    print('No more comments to scroll through.')
                    break_d += 1
                else:
                    print("last_height-Before:",last_height)
                    last_height = browser.execute_script("return document.body.scrollHeight")
                    print("last_height-After:",last_height)
            
            else:
                break_d += 1
                print('No comment elements found')
        else:
            print('comment_elements is not defined')
        if 'break_d' in locals() and break_d > 5:
            break
    browser.implicitly_wait(.5)
    # unique_comments = []
    # seen = set()
    # for comment in comments_for_scrap:
    #     comment_data = (comment.user_pro_pic, comment.comment_time, comment.user_name, comment.user_profile_url, comment.comment_text)
    #     if comment_data not in seen:
    #         unique_comments.append(comment)
    #         seen.add(comment_data)
    return comments_for_scrap

def loading_checker(browser):
    while True:
            # Check for circular progress indicator
        try:
            print('loading_checker looking for progress_indicator')
            progress_indicator = browser.find_element(By.XPATH, os.getenv('PROGRESS_INDICATOR_PATH')).get_attribute("aria-label")
            print('---------------------------------progress_indicator:',progress_indicator)
            time.sleep(2)
        except:
            print('loading_checker progress_indicator not found')
            break


def comment_data_taker(browser, comments_for_scrap, comment_elements,visited_reply_links):
    
    for comment in comment_elements:
        try:
            reply_link = comment.find_element(By.XPATH, os.getenv('REPLY_LINK_PATH')).get_attribute("href")
        except:
            continue
        print('reply_link',reply_link)
        if reply_link in visited_reply_links:
            print('Already visited reply link:',reply_link)
            continue
        visited_reply_links.append(reply_link)



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
            
            try:
                no_com_rep = parse_number_with_suffix(comment.find_element(By.XPATH, os.getenv('COMMENT_REPLY_COUNT')).text)
                extract_replies(browser, no_com_rep, reply_link, comments_replies_list,visited_reply_links)

            except Exception as e:
                # print(f"Error retrieving comment replies: {e}")
                no_com_rep = 0
                print('no_com_rep',no_com_rep)
            

            
                # print('comments_replies_list',comments_replies_list)
            comments_for_scrap.append(Comment(user_pro_pic, comment_time, user_name, user_profile_url, comment_text, comments_replies_list))
            # print('Comments',comments_for_scrap)
        except Exception as e:
            print(f"Error processing comment link: {e}")


def extract_replies(browser, no_com_rep, reply_url, comments_replies_list, visited_reply_links):
    try:
        # Store the original window handle
        original_window = browser.current_window_handle
        
        # Open new tab
        browser.execute_script(f"window.open('{reply_url}');")
        browser.switch_to.window(browser.window_handles[-1])

        loading_checker(browser)
        
        
        print("Switched to reply tab:", browser.title)
        try:
            break_d = 0
            last_height = browser.execute_script("return document.body.scrollHeight")
            print('last_height:', last_height)
            
            for _ in range(0, int(no_com_rep)):
                browser.implicitly_wait(.5)
                loading_checker(browser)
                comment_elements = browser.find_elements(By.XPATH, os.getenv('COMMENT_PATH'))
                comment_elements = comment_elements[1:]
                reply_data_taker(comments_replies_list, comment_elements, visited_reply_links)
                click_show_more(browser)
                
                if 'comment_elements' in locals():
                    if len(comment_elements) > 0:
                        browser.execute_script("arguments[0].scrollIntoView(true);", comment_elements[-1])
                        if last_height == browser.execute_script("return document.body.scrollHeight"):
                            print('No more comments to scroll through.')
                            break_d += 1
                        else:
                            print("last_height-Before:", last_height)
                            last_height = browser.execute_script("return document.body.scrollHeight")
                            print("last_height-After:", last_height)
                    else:
                        break_d += 1
                        print('No comment elements found')
                else:
                    print('comment_elements is not defined')
                    
                if 'break_d' in locals() and break_d > 5:
                    break
        except Exception as e:
            print(f"Error in extract_replies: {e}")
            pass
            
        # Close only the reply tab
        print("Closing reply tab")
        browser.close()
        
        # Switch back to original tab
        print('Switching back to original tab')
        browser.switch_to.window(original_window)
        print("Back to original tab:", browser.title)
        
    except Exception as e:
        print(f"Error in extract_replies: {e}")
        # Make sure we switch back to original window even if there's an error
        try:
            for handle in browser.window_handles:
                if handle != original_window:
                    browser.switch_to.window(handle)
                    browser.close()
            browser.switch_to.window(original_window)
        except:
            pass


def remove_duplicate_comments(comments_replies_list):
    unique_comments = []
    seen = set()
    print('comments_replies_list:',len(comments_replies_list))
    for comment in comments_replies_list:
        comment_data = (comment.user_pro_pic, comment.comment_time, comment.user_name, comment.user_profile_url, comment.comment_text)
        if comment_data not in seen:
            unique_comments.append(comment)
            seen.add(comment_data)
    comments_replies_list = unique_comments
    print('comments_replies_list:',len(comments_replies_list))
    
def reply_data_taker(comments_replies_list, comment_elements,visited_reply_links):
    for comment in comment_elements:
        try:
            reply_link = comment.find_element(By.XPATH, os.getenv('REPLY_LINK_PATH')).get_attribute("href")
            print('reply_link',reply_link)
            if reply_link in visited_reply_links:
                print('Already visited reply link:',reply_link)
                continue
            visited_reply_links.append(reply_link)
        except:
            continue
        
        try:
            user_name = comment.find_element(By.XPATH, os.getenv('USER_NAME_PATH')).text
            # print('reply_user_name:',user_name)
            user_pro_pic = comment.find_element(By.XPATH, os.getenv('USER_PRO_PIC_PATH')).get_attribute("src").replace("_bigger", "")
            # print('reply_user_pro_pic:',user_pro_pic)
            user_profile_url = comment.find_element(By.XPATH, os.getenv('USER_PROFILE_URL_PATH')).get_attribute("href")
            # print('reply_user_profile_url:',user_profile_url)

            try:
                comment_text = comment.find_element(By.XPATH, os.getenv('COMMENT_TEXT_PATH')).text
                # print('reply_comment_text:',comment_text)
            except Exception as e:
                print(f"Error retrieving comment text:")
                comment_text = ""
            comment_time = timeChange(comment.find_element(By.XPATH, os.getenv('COMMENT_TIME_PATH')).get_attribute("datetime"))
            # print('reply_comment_time:',comment_time)
            comments_replies_list.append(Comment(user_pro_pic, comment_time, user_name, user_profile_url, comment_text, []))
            # print('reply_comments_replies_list:',len(comments_replies_list))
        except Exception as e:
            print(f"Error processing comment link: {e}")



def read_source(file_path="source.json"):
    """Read and return the content of the source JSON file."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            # print("Loaded JSON content.")
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
            print(login(
                browser,
                "aleya98337",
                "Test@123!",
            ))
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
                print('1',scrap_data)
                print(json.dumps(scrap_data.to_json()))
            except Exception as e:
                print(f"Error scraping post: {e}")
                print(scrap_data)
                continue
            if scrap_data is None:
                print(f"No data scraped for link {xlink}. Skipping...")
                continue
            # print('2', scrap_data)
            file_name = f"{xlink.split('/')[-3]}_{xlink.split('/')[-1]}"
            with open(f"post_data/{file_name}.json", "w", encoding="utf-8", errors="replace") as json_file:
                json_file.write(scrap_data.to_json())
            print(f"Scraped and saved post {file_name}")
        except Exception as e:
            print(f"Error processing link {xlink}: {e}")    



if __name__ == "__main__":
    main()