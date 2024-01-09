from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys
import Account as ac
from selenium.webdriver.common.keys import Keys
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('--lang=en-US')

service = Service('YOUR CHROME DRIVER PATH')
driver = webdriver.Chrome(options=chrome_options, service=service)
driver.get("https://www.twitter.com/")


def login():
    login_btn = driver.find_element(By.XPATH,
                                    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a/div')
    login_btn.click()
    time.sleep(2)
    username = driver.find_element(By.XPATH, '//input[@name="text"]')
    username.send_keys(ac.username)
    username.send_keys(Keys.RETURN)
    time.sleep(2)
    password = driver.find_element(By.XPATH, '//input[@name="password"]')
    password.send_keys(ac.password)
    password.send_keys(Keys.RETURN)
    time.sleep(5)


def search():
    search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
    search_box.send_keys('YOUR SEARCH KEYWORD')
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)
    latest = driver.find_element(By.XPATH, "//span[contains(text(),'Latest')]")
    latest.click()


def tweets():
    UserTags = []
    TimeStamps = []
    Tweets = []
    Replys = []
    reTweets = []
    Likes = []

    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    while True:
        for article in articles:
            UserTag = driver.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
            UserTags.append(UserTag)

            TimeStamp = driver.find_element(By.XPATH, ".//time").get_attribute('datetime')
            TimeStamps.append(TimeStamp)

            Tweet = driver.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
            Tweets.append(Tweet)

            Reply = driver.find_element(By.XPATH, ".//div[@data-testid='reply']").text
            Replys.append(Reply)

            reTweet = driver.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
            reTweets.append(reTweet)

            Like = driver.find_element(By.XPATH, ".//div[@data-testid='like']").text
            Likes.append(Like)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(3)
        articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        Tweets2 = list(set(Tweets))
        if len(Tweets2) > 5:
            df = pd.DataFrame(zip(UserTags, TimeStamps, Tweets, Replys, reTweets, Likes),
                              columns=['UserTags', 'TimeStamps', 'Tweets', 'Replys', 'reTweets', 'Likes'])
            df.to_excel("tweets.xlsx")
            exit()


if __name__ == '__main__':
    login()
    time.sleep(2)
    search()
    time.sleep(2)
    tweets()
    time.sleep(10000)
    sys.exit('Program finished.')
