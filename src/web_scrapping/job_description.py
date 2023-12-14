# --------- import necessary modules -------
# For webscraping
from bs4 import BeautifulSoup

# Parsing and creating xml data
from lxml import etree as et

# Store data as a csv file written out
from csv import writer

# In general to use with timing our function calls to Indeed
import time

# Assist with creating incremental timing for our scraping to seem more human
from time import sleep

# Dataframe stuff
import pandas as pd

# Random integer for more realistic timing for clicks, buttons and searches during scraping
from random import randint

# Multi Threading
import threading

# Threading:
from concurrent.futures import ThreadPoolExecutor, wait

import selenium

from selenium import webdriver

# Starting/Stopping Driver: can specify ports or location but not remote access
from selenium.webdriver.chrome.service import Service as ChromeService

# Manages Binaries needed for WebDriver without installing anything directly
from webdriver_manager.chrome import ChromeDriverManager

# Allows searchs similar to beautiful soup: find_all
from selenium.webdriver.common.by import By

# Try to establish wait times for the page to load
from selenium.webdriver.support.ui import WebDriverWait

# Wait for specific condition based on defined task: web elements, boolean are examples
from selenium.webdriver.support import expected_conditions as EC

# Used for keyboard movements, up/down, left/right,delete, etc
from selenium.webdriver.common.keys import Keys

# Locate elements on page and throw error if they do not exist
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome()
# Allows you to cusotmize: ingonito mode, maximize window size, headless browser, disable certain features, etc
option = webdriver.ChromeOptions()

# Setting options like incognito mode
option.add_argument("--incognito")

# If you want to use headless mode
# option.add_argument("--headless")

# Creating a Chrome WebDriver instance with these options
driver = webdriver.Chrome(options=option)

# Define job and location search keywords


# Finding location, position, radius=35 miles, sort by date and starting page
paginaton_url = 'https://de.indeed.com/jobs?q={}&l={}&radius=35&filter=0&lang=en&sort=date&start={}'

# print(paginaton_url)

start = time.time()

job_ = 'Data+Engineer'
location = 'Munich'

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)


driver.get(paginaton_url.format(job_, location, 0))

sleep(randint(2, 6))
job_description_list = []
for i in range(0,max_iter_pgs):
    driver.get(paginaton_url.format(job_,location,i*10))

    sleep(randint(2, 4))

    job_page = driver.find_element(By.ID,"mosaic-jobResults")
    jobs = job_page.find_elements(By.CLASS_NAME,"job_seen_beacon") # return a list

    for jj in jobs:
        job_title = jj.find_element(By.CLASS_NAME,"jobTitle")


        # Click the job element to get the description
        job_title.click()

        # Help to load page so we can find and extract data
        sleep(randint(3, 5))

        try:
            job_description_list.append(driver.find_element(By.ID,"jobDescriptionText").text)

        except:

            job_description_list.append(None)
driver.quit()
# job_description_list[-17:-1]