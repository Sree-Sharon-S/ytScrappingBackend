from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import os

def getYoutubeSite(channel_link, no):
        channel_link = channel_link + "/videos"
        urls_list = []
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--no-sandbox")
        option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(service=Service(os.environ.get(" CHROMEDRIVER PATH")), option = option)
        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        
        driver.get(channel_link)
        time.sleep(3)
        print("entered into videos")
        scrolled_height = 0
        while True:
            print(scrolled_height)
            driver.execute_script(f"window.scrollTo({scrolled_height},{scrolled_height+int(500000)})")
            time.sleep(5)
            scrolled_height += 500000
            print("finding elements")
            soup = BeautifulSoup(driver.page_source,'html.parser')
            elements_found = soup.select("#items > ytd-grid-video-renderer > div > ytd-thumbnail > a")

            print("no of elements found is " + str(len(elements_found)))
            
            if len(elements_found) >= no:
        
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
