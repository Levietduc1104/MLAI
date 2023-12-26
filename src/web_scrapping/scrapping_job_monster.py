# --------- import necessary modules -------
# For webscraping
# from bs4 import BeautifulSoup

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
import pandas as pd

# Allows you to cusotmize: ingonito mode, maximize window size, headless browser, disable certain features, etc
option = webdriver.ChromeOptions()

# Setting options like incognito mode
option.add_argument("--incognito")

# If you want to use headless mode
# option.add_argument("--headless")

# Creating a Chrome WebDriver instance with these options
driver = webdriver.Chrome(options=option)

# Finding location, position, radius=35 miles, sort by date and starting page


paginaton_url = 'https://www.stepstone.de/jobs/{}?action=facet_selected%3bdetectedLanguages%3ben&fdl=en'
# print(paginaton_url)

start = time.time()

job_ = 'software-developer'
location = ''

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

driver.get(paginaton_url.format(job_, location, 0))

sleep(randint(2, 6))

p=driver.find_element(By.CLASS_NAME,'res-vurnku.at-facet-header-total-results').text

# Max number of pages for this search! There is a caveat described soon
max_iter_pgs=int(p.split(' ')[0])//25
print(max_iter_pgs)

job_lst = []
job_description_list_href = []

# job_description_list =  []
job_title = []
job_location = []
job_data = []
salary_list = []
job_page = None
job_description_list = []

option = webdriver.ChromeOptions()
# Add any necessary Chrome options here

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

sleep(randint(2, 6))

job_description_list: list  = []
job_description: list = None
company_name:list = None

for i in range(4):  # Loop through the first two pages
    driver.get(paginaton_url.format(job_, location, i * 10))
    time.sleep(randint(2, 4))
    # Collecting all job links
    # Wait up to 10 seconds for the jobs container to become available
    job_page = driver.find_element(By.CLASS_NAME, "res-81xrsn")

    # Find all job elements
    jobs = job_page.find_elements(By.CLASS_NAME, "res-urswt")
    job_links = [job.find_element(By.CSS_SELECTOR, "a.res-y456gn").get_attribute('href') for job in jobs]
    for job_link in job_links:

     driver.get(job_link)
     time.sleep(randint(3, 5))

     try:
          wait = WebDriverWait(driver, 10)
          job_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "listing-content-provider-bewwo"))).text
          job_description = driver.find_element(By.CLASS_NAME, "js-app-ld-ContentBlock").text
          company_name_element = driver.find_element(By.CLASS_NAME, "listing-content-provider-lxa6ue")
          company_name = company_name_element.text
          job_location_element = driver.find_element(By.CLASS_NAME, "listing-content-provider-1whr5zf")
          company_location = job_location_element.text
          job_desc_container = driver.find_element(By.CLASS_NAME, 'listing-content-provider-i9ybor')

          # Within this container, find all the div elements that might contain parts of the job description
          job_desc_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "listing-content-provider-14ydav7")))

          # Initialize a variable to hold the full job description
          job_description_full = ''

          # Iterate through the found elements and concatenate their text
          for element in job_desc_elements:
               job_description_full += element.text + '\n'

          # Print the full job description
          job_description_list.append((job_title, job_description_full, company_name, company_location, job_link))
          print("-------------------------------------------------")
          print(job_description_full.strip())  # .strip() to remove leading/trailing whitespace

     except Exception as e:

          print(f"Error accessing job description: {e}")
          job_description_list.append(None)
df = pd.DataFrame(job_description_list, columns=['Job Title', 'Job Description', 'Company Name', 'Location', 'Job Link'])
csv_filename = 'job_listings_monster.csv'
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")
print(job_description_list)
driver.quit()

