from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # Import the By class
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

driver = webdriver.Chrome()
driver.get("https://de.indeed.com/?r=us")

print(driver.title)

# Use the "By" class to locate the search input element
search = driver.find_element(By.ID, "text-input-what")

# try:
#     close_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.YOUR_LOCATOR_TYPE, "YOUR_LOCATOR_VALUE"))
#     )
#     close_button.click()
# except Exception as e:
#     print(f"Failed to close the pop-up: {e}")

search.send_keys("test")

search.send_keys(Keys.RETURN)
time.sleep(5)
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "mosaic-jobResults"))
    )
    print(main.text)
except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()


driver.quit()