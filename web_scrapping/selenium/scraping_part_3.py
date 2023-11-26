from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # Import the By class
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

driver = webdriver.Chrome()
driver.get("https://orteil.dashnet.org/cookieclicker/")

try:
    # Wait until the element is present and clickable
    consent_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[@class='fc-button-label' and text()='Consent']"))
    )
    consent_button.click()  # Click the element once it's clickable

    lang_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "langSelect-EN"))
    )
    lang_button.click()

    driver.implicitly_wait(5)
    cookies = driver.find_element(By.ID, "bigCookie")

    cookie_count = driver.find_element(By.ID, "cookies")

    items = [driver.find_element(By.ID, "productPrice" + str(i)) for i in range(1, 0, -1)]

    actions = ActionChains(driver)
    actions.click(cookies)


    for i in range (5000):
        actions.perform()

        # time.sleep(1)
        # print("actions")
    #     count = cookie_count.text
    #     for item in items:
    #         value = int(item.text)
    #         if value <= count:
    #             upgrade_actions = ActionChains(driver)
    #             upgrade_actions.move_to_elements(item)
    #             upgrade_actions.click()

except Exception as e:
    print(f"Error: {e}")
    driver.quit()