from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # Import the By class
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
# /Users/levietduc/Documents/Learning/CV/Scanning/src/selenium/scrapping_part_2.py
driver = webdriver.Chrome()
driver.get("https://www.techwithtim.net/")

# Find an element by its link text
link = driver.find_element(By.LINK_TEXT, "Tutorials")
link.click()
try:
    ml_image_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Machine Learning with Python' and @class='tutorial__TutorialCardImage-sc-1rebzxr-2 hBRhHJ']"))
    )

    # Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView();", ml_image_element)

    # Give a short pause to allow any potential animations or changes on the page
    time.sleep(1)

    # Now, attempt the click
    ml_image_element.click()

    introduction_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Introduction')]"))
    )
    print("finding button")
    # Click the button
    introduction_button.click()
    driver.back()
    driver.back()
    driver.back()
    time.sleep(5)
    # button_element.click()
    print("done")


except Exception as e:
    print(f"Error: {e}")
    driver.quit()

# search = driver.find_element(By.ID, "text-input-what")

# # try:
# #     close_button = WebDriverWait(driver, 10).until(
# #         EC.element_to_be_clickable((By.YOUR_LOCATOR_TYPE, "YOUR_LOCATOR_VALUE"))
# #     )
# #     close_button.click()
# # except Exception as e:
# #     print(f"Failed to close the pop-up: {e}")

# search.send_keys("test")

# search.send_keys(Keys.RETURN)
# time.sleep(5)
# try:
#     main = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "mosaic-jobResults"))
#     )
#     print(main.text)
# except Exception as e:
#     print(f"An error occurred: {e}")
#     driver.quit()


driver.quit()