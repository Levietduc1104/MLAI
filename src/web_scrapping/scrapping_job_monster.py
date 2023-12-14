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
paginaton_url = 'https://de.indeed.com/jobs?q={}&l={}&radius=35&filter=0&lang=en&sort=date&start={}'

# print(paginaton_url)

start = time.time()

job_ = 'Data+Engineer'
location = 'Munich'

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

driver.get(paginaton_url.format(job_, location, 0))

sleep(randint(2, 6))

p=driver.find_element(By.CLASS_NAME,'jobsearch-JobCountAndSortPane-jobCount').text

# Max number of pages for this search! There is a caveat described soon
max_iter_pgs=int(p.split(' ')[0])//15


job_lst = []
job_description_list_href = []

# job_description_list =  []
job_title = []
job_location = []
job_data = []
salary_list = []

job_description_list = []

option = webdriver.ChromeOptions()
# Add any necessary Chrome options here

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)

sleep(randint(2, 6))

job_description_list = []
job_description = None
company_name = None

for i in range(2):  # Loop through the first two pages
    driver.get(paginaton_url.format(job_, location, i * 10))
    time.sleep(randint(2, 4))

    # Collecting all job links
    job_page = driver.find_element(By.ID, "mosaic-jobResults")
    jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")
    job_links = [job.find_element(By.CSS_SELECTOR, "a").get_attribute('href') for job in jobs]

    for job_link in job_links:
        # Navigate to job link
        driver.get(job_link)
        time.sleep(randint(3, 5))
        print(job_link)
        # Process job description
        try:
            wait = WebDriverWait(driver, 10)
            job_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))).text
            job_description = driver.find_element(By.ID, "jobDescriptionText").text
            company_name_element = driver.find_element(By.XPATH, "//div[@data-company-name='true']/span/a")
            company_name = company_name_element.text

            company_location_element = driver.find_element(By.XPATH, "//div[@data-testid='inlineHeader-companyLocation']/div")
            company_location = company_location_element.text
            job_description_list.append((job_title, job_description, company_name, company_location, job_link))
            # print(company_location)


        except Exception as e:
            print(f"Error accessing job description: {e}")
            job_description_list.append(None)

        # Navigate back to the job list page
        driver.get(paginaton_url.format(job_, location, i * 10))
        time.sleep(randint(2, 4))
df = pd.DataFrame(job_description_list, columns=['Job Title', 'Job Description', 'Company Name', 'Location', 'Job Link'])
csv_filename = 'job_listings.csv'
df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")
print(job_description_list)
driver.quit()
