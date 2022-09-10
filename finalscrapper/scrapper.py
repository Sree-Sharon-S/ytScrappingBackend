from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from pytube import YouTube
import os
from finalscrapper.urlgen import create_presigned_url, s3_signature
from finalscrapper.db2 import db, YtScrape,comments
from finalscrapper.aws_s3 import client
#from finalscrapper import collection
from datetime import datetime


def Scrape(urls):
    for url in urls: 
        #option = webdriver.ChromeOptions()
        #option.add_argument("--headless")
        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--no-sandbox")
        option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(service=Service(os.environ.get(" CHROMEDRIVER PATH")), options = option)
  

        
        
        driver.get(url)
        time.sleep(5)

        prev_h = 500
        
        driver.execute_script(f"window.scrollTo({0},{600})")
        time.sleep(5)
        try:     
            driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]')
            
            tot_com = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text
        except:
            tot_com = 1

        while True: #while loopdfor page height
            height = driver.execute_script("""
                        function getActualHeight(){
                            return Math.max(
                                Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                                Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                                Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                            );
                        }
                        return getActualHeight();
                    """)
            present_height = height
            if prev_h >= present_height:
                break
            driver.execute_script("window.scrollTo({},{} )".format(prev_h,height+1000))
            print("Scrolling")
            time.sleep(1)
            prev_h = height
            
            
        soup = BeautifulSoup(driver.page_source,'html.parser')
        
        tot_comments = 0
        comment_div = soup.select('#content #content-text')
        comment_list = [x.text for x in comment_div]
        commentater_div = soup.select('#author-text > span')
        commentater_list = [x.text for x in commentater_div]
        try:
            comments_div=soup.select_one('#header > ytd-comments-header-renderer > div > h2 > yt-formatted-string >span')
            if comments_div != None:
                tot_comments = comments_div.text
            elif comment_div == None:
                tot_comments = soup.select_one('#header > ytd-comments-header-renderer > div > h2 > yt-formatted-string').text
        except:
            tot_comments = 0
            

        title_text_div = soup.select_one('#container > h1 > yt-formatted-string') 
        title = title_text_div and title_text_div.text   
        likes_div = soup.select('#top-level-buttons-computed > ytd-toggle-button-renderer > a > yt-formatted-string')
            
        if len(likes_div)!=0:
            likes = likes_div[0].text  or  "--"
        else: 
            likes = "Reload"
        yt = YouTube(url)
        thumbnail = yt.thumbnail_url
        views = yt.views
        print(yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first())
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first().download()
        
        for file in os.listdir():
            if '.mp4' in file:
                upload_file_key = 'videos/' + str(file) 
                client.upload_file(file, 'scrappernew', upload_file_key)
                generated_signed_url = create_presigned_url('scrappernew', 'videos/'+str(file), 604800, s3_signature['v4'])
                
                os.remove(str(file))


        scrapeobj = YtScrape(video_url=str(url), thumbnail_urls=str(thumbnail), title=str(title), likes=str(likes), no_of_comments=tot_com, views=views,download_link= str(generated_signed_url))
        db.session.add(scrapeobj)
        db.session.commit()
                             
        for i in range (len(commentater_list)):
            commentsobj = comments(title=str(title), commentators=commentater_list[i], comments=comment_list[i])
            db.session.add(commentsobj)
            db.session.commit()
        
        created_time = datetime.datetime.now()
'''
        mongodata = {
            'created':created_time,
            'title': str(title),
            'video link':str(url),
            'thumbnail':str(thumbnail),
            'views':views,
            'total comments':tot_com,
            'download':str(generated_signed_url),
            'likes': str(likes)
        }

        collection.insert_one(mongodata)

    '''    





