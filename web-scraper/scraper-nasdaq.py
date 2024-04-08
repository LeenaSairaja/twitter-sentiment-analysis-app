from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# from bs4 import BeautifulSoup
# import requests
import re
from typing import List

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# driver: webdriver = webdriver.Chrome()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver: WebElement = webdriver.Chrome(options=options)

def get_nasdaq_headlines(ticker: str="tsla"):
    ticker=ticker.lower()
    driver.get(f"https://www.nasdaq.com/market-activity/stocks/{ticker}/news-headlines")

    df=pd.DataFrame({'headlines':[]})

    pages=10
    c=0

    time.sleep(1)
    
    for page in range(pages):
        for i in range(1,8): # 1 to 7
            xpath=f'/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/ul/li[{i}]/a/p'

            try:
                element = driver.find_element(by=By.XPATH, value=xpath)
                print(f"headline {c+i}: "+ element.text)

                # add to dataframe
                df.loc[len(df.index)] = [element.text]  
            except Exception as e:
                print("error")
                print(e)
                exit()
        
        # go to next set of headlines
        nextButton: WebElement = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/button[2]")
        # nextButton=driver.find_element(by=By.CLASS_NAME,value="pagination__next")
        # nextButton=driver.find_element(by=By.ID,value="onetrust-accept-btn-handler")
        nextButton.click()

        time.sleep(2)

        c+=7
        print()
        print("Next page")
        print()
    
    # save the df to csv file
        
    df.to_csv(f'{ticker}_dealines.csv')

if __name__ == "__main__":
    get_nasdaq_headlines("TSLA")
    input("Press enter to quit... ")
