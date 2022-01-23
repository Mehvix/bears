import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

import gspread
from oauth2client.service_account import ServiceAccountCredentials

###########
# Scraper #
###########

URL = "https://safe.density.io/#/displays/dsp_956223069054042646?token=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e"
TIMEOUT = 10

# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox()


def getCapacity() -> int:
    driver.get(URL)

    try:
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'span'))
        WebDriverWait(driver, TIMEOUT).until(element_present)
        value = driver.find_element_by_css_selector(
            "#root > div > div > div.styles_main__3Ul1n.styles_sidebarOpen__1t7th > div.styles_waitTimeFullnessWrapper__3PRdQ > div > span"
        ).text
        # print(value)
        value = int(value.split("%")[0])
        return value
    except TimeoutException:
        print("Timed out waiting for page to load!")
        return -1


############
# Database #
############

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("secret.json", SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(
    "1KqE5Pk76Wc9hizXjJeClh_oZwjqtYbetqRLfvxZerJ4").sheet1


def append(content):
    print(f"Adding entry: {content}")
    sheet.append_row(content)


while True:
    append([str(datetime.datetime.now()), getCapacity()])
    time.sleep(300 - time.time() % 300)
