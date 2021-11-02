import os
import shutil
import subprocess
import sys
import time
from msvcrt import getch
from time import sleep

import chromedriver_autoinstaller
import youtube_dl
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

try:
    shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

option = webdriver.ChromeOptions()
option.add_argument("headless")
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
driver.implicitly_wait(10)


def vidstrip(playlist):
    for i in range(len(playlist)):
        end=playlist[i].find("&")
        playlist[i]=playlist[i][:end]
    return playlist


def download():
    ydl_opts = {} 

    body = driver.find_element_by_css_selector('body')
    for i in range(5):
        body.send_keys(Keys.PAGE_DOWN)
    time.sleep(5)
    playlist=[]
    videos=[]
    videos=driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')

    for video in videos:
        link=video.find_element_by_xpath('.//*[@id="thumbnail"]/a').get_attribute("href")
        playlist.append(link)

    vidlist=vidstrip(playlist)
    os.chdir('D:\youtube') 

    for link in vidlist:
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)
    driver.close()



def login(username, password):       # Logs in the user
    driver.get("https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620")


    try:
        WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located(
            (By.ID, "Email"))).send_keys(username)      # Enters username
    except TimeoutException:
        del username
        driver.quit()
    WebDriverWait(driver, 60).until(expected_conditions.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[2]/div[2]/div[1]/form/div/div/input"))).click()      # Clicks NEXT
    time.sleep(0.5)

    try:
        try:
            WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located(
                (By.ID, "password"))).send_keys(password)       # Enters decoded Password
        except TimeoutException:
            driver.quit()
        WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(
            (By.ID, "submit"))).click()     # Clicks on Sign-in
    except TimeoutException or NoSuchElementException:
        print('\nUsername/Password seems to be incorrect, please re-check\nand Re-Run the program.')
        del username, password
        driver.quit()

    try:
        print('\nLogin Successful!\n')

        driver.get("https://www.youtube.com/playlist?list=LL")


    except TimeoutException:
        print('\nUsername/Password seems to be incorrect, please re-check\nand Re-Run the program.')
        del username, password
        driver.quit()

USERNAME = "email"
PASSWORD = "password"

# Assign drivers here.

stealth(driver,
        user_agent='DN',
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )       # Before Login, using stealth

login(USERNAME, PASSWORD)       # Call login function/method

stealth(driver,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )       # After logging in, revert back user agent to normal.

# Redirecting to Google Meet Web-Page
time.sleep(2)

download()
