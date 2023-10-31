from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.options import Options
from icecream import ic

options = Options()
options.add_argument("-headless")

driver = webdriver.Firefox(options=options)
ic("headless inicialized")
driver.get('https://www.instagram.com/josef.jindra.666/')
try:
    time.sleep(5)
    click = driver.find_element(By.CSS_SELECTOR,'button._a9--:nth-child(2)')
    click.click()
    time.sleep(5)
except Exception:
    print("Failed to contant instagram servers. Please try again later.")
search = driver.find_element(By.CSS_SELECTOR,'h1._aacl')
print(search.text)
time.sleep(100)

