import time
from http.cookiejar import Cookie
import requests as requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
rki_dashboard = "https://digi4school.at/"
driver.get(rki_dashboard)

try:
    emailField = driver.find_element_by_id("email")
    emailField.send_keys("sascha.gottsbacher@aon.at")

    passwordField = driver.find_element_by_id("password")
    passwordField.send_keys("BOnqRqMyP1PKWdD8OOtZ")

    passwordField.send_keys(Keys.ENTER)

    time.sleep(1)

    driver.get("https://a.digi4school.at/ebook/5134/?page=24")
    button = driver.find_element(By.ID, "btnZoomHeight")
    button.click()
    time.sleep(0.5)
    img = driver.find_element(By.ID, "pg24")

    img.screenshot("p24.png")

finally:
    driver.quit()

