from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import urllib


driver = webdriver.Chrome()


def openbrowser(locid, key):
    driver.wait = WebDriverWait(driver, 10)
    driver.maximize_window()
    words = key.split()
    txt =''
    for w in words:
        txt +=(w+'+')
    driver.get("https://www.glassdoor.co.in/Job/new-delhi-india-software-testing-jobs-SRCH_IL.0,15_IC2891681_KO16,32.htm")
    return driver

def geturl(driver):
    urls = set()
    while True:
        # print(len(urls))
        if len(urls) >= 20:
            break
        soup1 = BeautifulSoup(driver.page_source, "lxml")
        main = soup1.find_all("li", {"class": "jl"})
        print("soup1.prettify()",soup1.prettify())  # Print the entire HTML content to check if it's loaded correctly.
        print("main",main)  # Print the main variable to check if it's capturing the correct elements.
        print("urls",urls)
        for m in main:
            urls.add('https://www.glassdoor.co.in{}'.format(m.find('a')['href']))
        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button'][data-role-variant='primary']"))
            )
            next_button.click()

            time.sleep(50)
        except (NoSuchElementException, ElementClickInterceptedException):
            driver.quit()
            break

    return list(urls)


x =openbrowser(locid =4477468, key='software testing')
with open('url_software_testing_loc_bangalore.json','w') as f:
    json.dump(geturl(driver),f, indent = 4)
    print("file created")