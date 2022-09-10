from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def getYoutubeSite(channel_link, no):
        channel_video_link = str(channel_link)+"/videos"
        urls_list = []
        option = webdriver.ChromeOptions()
        #option.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        driver.get(channel_video_link)
        time.sleep(3)
        print("entered into videos")
        scrolled_height = 0
        while True:
            print("the scrolled_height now is" + str(scrolled_height))
            driver.execute_script(f"window.scrollTo({scrolled_height},{scrolled_height+int(5000)})")
            time.sleep(5)
            scrolled_height += 5000
            print("finding elements")
            soup = BeautifulSoup(driver.page_source,'html.parser')
            elements_found = soup.select("#items > ytd-grid-video-renderer > div > ytd-thumbnail > a")

            print("no of elements found is " + str(len(elements_found)))
            
            if len(elements_found) >= no:
                driver.quit()    
                for url in elements_found:
                    urls_list.append("https://www.youtube.com"+str(url["href"]))
                    print("fetching links")
                break
            else:
                print("searching for more elements")
                
        print("got more elements")    
        while True:
            urls_list.pop()
            print("deleting unwanted elements")
            if len(urls_list) == no:
                break
        print("these are the collected links")
        print(urls_list)
        return urls_list

li = getYoutubeSite('https://www.youtube.com/c/musicwithnopain/videos',70)