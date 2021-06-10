
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
import time 
import youtube_dl 
import os
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller
import subprocess
import shutil

from selenium_stealth import stealth
from msvcrt import getch


try:
    shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

## 경로 설정을 따로 하지 않고 크롬 설치시 아래 경로가 기본값
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')


option = Options()
## 9222포트로 크롬을 염
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
driver.implicitly_wait(10)

## 추출한 url에서 & 앞까지 끊어줌
def vidstrip(playlist):
    for i in range(len(playlist)):
        end=playlist[i].find("&")
        playlist[i]=playlist[i][:end]
    return playlist


def download():
    ydl_opts = {} 

## 한페이지에 로드 되는 영상이 100개인데 페이지 다운을 통해 모든 목록을 불러와야 전체 영상을 받을 수 있음
## page_down 버튼 클릭 횟수를 늘려줘서 내릴수 있음 50을 줬을땐 240까진 불러왔음
    body = driver.find_element_by_css_selector('body')
    for i in range(50):
        body.send_keys(Keys.PAGE_DOWN)
        
## 모든 영상 url 추출 과정
    time.sleep(5)
    playlist=[]
    videos=[]
    videos=driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')

    for video in videos:
        link=video.find_element_by_xpath('.//*[@id="thumbnail"]/a').get_attribute("href")
        playlist.append(link)

## url 수정 과정
    vidlist=vidstrip(playlist)
    count=1
## 영상이 저장될 위치
    os.chdir('D:\youtube') 

## youtube_dl을 통해 영상을 하나씩 다운받음
    for link in vidlist:
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])    
        except:
            print("Exception occured. Either the video has no quality as set by you, or it is not available. Skipping video {number}".format(number = count))
            continue
        count += 1
    driver.close()


## 로그인
def login(username, password):     
    driver.get("https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620")
    try:
        WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located(
            (By.ID, "Email"))).send_keys(username)   
    except TimeoutException:
        del username
        driver.quit()
    WebDriverWait(driver, 60).until(expected_conditions.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[2]/div[2]/div[1]/form/div/div/input"))).click()   
    time.sleep(0.5)

    try:
        try:
            WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located(
                (By.ID, "password"))).send_keys(password)      
        except TimeoutException:
            driver.quit()
        WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(
            (By.ID, "submit"))).click()   
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


USERNAME = input("User Name : ")
PASSWORD = input("Password : ")

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# stealth 기능

stealth(driver,
        user_agent='DN',
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )       # Before Login, using stealth

login(USERNAME, PASSWORD)       

stealth(driver,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )       


time.sleep(2)

download()
