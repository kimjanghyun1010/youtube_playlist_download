from selenium import webdriver
import time 
import youtube_dl 
import os
from time import sleep
from bs4 import BeautifulSoup as bs


driver = webdriver.Chrome(executable_path='./chromedriver')

soup = bs(driver.page_source, 'html.parser')


driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
sleep(3)
driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
driver.find_element_by_id('identifierId').send_keys('your google ID')
driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
sleep(3)
driver.find_element_by_xpath('//input[@type="password"]').send_keys('your goolge PW')
driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
sleep(2)
driver.get('https://www.youtube.com/playlist?list=LL')
sleep(5)



ydl_opts = {} 

def vidstrip(playlist):
    for i in range(len(playlist)):
        end=playlist[i].find("&")
        playlist[i]=playlist[i][:end]
    return playlist


# url = input("Enter youtube playlist link : ")
# driver = webdriver.Chrome() 
# driver.get(url)
time.sleep(5)
playlist=[]
videos=driver.find_elements_by_class_name('style-scope ytd-playlist-video-renderer')
for video in videos:
    link=video.find_element_by_xpath('.//*[@id="content"]/a').get_attribute("href")
    playlist.append(link)
    
vidlist=vidstrip(playlist)
count=1
os.chdir('C:/Users/mskjh/Downloads') 

for link in vidlist:
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except:
        print("Exception occured. Either the video has no quality as set by you, or it is not available. Skipping video {number}".format(number = count))
        continue
    count += 1

driver.close()
