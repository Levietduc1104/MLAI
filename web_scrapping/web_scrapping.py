from bs4 import BeautifulSoup
import requests
from random import random
from time import sleep
from email.message import EmailMessage
from collections import namedtuple
import smtplib
import csv


def generate_url(job_title, job_location):
    url_template = "https://de.indeed.com/jobs?q={}&l={}"
    url = url_template.format(job_title, job_location)
    return url

url = generate_url("python", "Augsburg")
response = requests.get(url)
print(response.reason)
soup = BeautifulSoup(response.text, 'html.parser')
job_listing_elements = soup.find_all('div', class_='jobCard_mainContent')
# Extract and print job title
card = job_listing_elements[0]
atag = card.h2.a
job_title = atag.get('title')
job_url = 'https://www.indeed.com' + atag.get('href')
