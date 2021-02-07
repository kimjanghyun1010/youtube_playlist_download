from selenium import webdriver
import time 
import youtube_dl 
import os
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys

## 크롬 드라이버 위치를 기입해서 알아서 크롬창을 띄울수 있게 함
driver = webdriver.Chrome(executable_path='./chromedriver')

## page 소스를 soup에 기록함
soup = bs(driver.page_source, 'html.parser')


## 접속 url
driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')

## 많은 요청을 지연없이 보내면 chrome에서 걸러낼수도 있기때문에 딜레이를 줘야함
sleep(3)

## id-button xpath
driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()

## id 입력 xpath
driver.find_element_by_id('identifierId').send_keys('your google ID')

## 패스워드 입력하러 가는 버튼 xpath
driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
sleep(3)

## 패스워드 입력 xpath
driver.find_element_by_xpath('//input[@type="password"]').send_keys('your goolge PW')

## 로그인 버튼
driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
sleep(2)

## youtube playlist url
driver.get('https://www.youtube.com/playlist?list=LL')
sleep(5)



ydl_opts = {} 


## 추출한 url에서 & 앞까지 끊어줌
def vidstrip(playlist):
    for i in range(len(playlist)):
        end=playlist[i].find("&")
        playlist[i]=playlist[i][:end]
    return playlist

## 한페이지에 로드 되는 영상이 100개인데 페이지 다운을 통해 모든 목록을 불러와야 전체 영상을 받을 수 있음
## page_down 버튼 클릭 횟수를 늘려줘서 내릴수 있음 50을 줬을땐 240까진 불러왔음
body = driver.find_element_by_css_selector('body')
for i in range(50):
    body.send_keys(Keys.PAGE_DOWN)
    ## sleep(2)



# url = input("Enter youtube playlist link : ")
# driver = webdriver.Chrome() 
# driver.get(url)



time.sleep(5)
## 모든 영상 url 추출 과정
playlist=[]
videos=driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')
for video in videos:
    link=video.find_element_by_xpath('.//*[@id="thumbnail"]/a').get_attribute("href")
    playlist.append(link)

    
## url 수정 과정
vidlist=vidstrip(playlist)
count=1

## 영상이 저장될 위치
os.chdir('C:/Users/mskjh/Downloads') 


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
