#!./venv/bin/python

import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager

import gspread
from oauth2client.service_account import ServiceAccountCredentials

###########
# Scraper #
###########

URL = "https://safe.density.io/#/displays/dsp_956223069054042646?token=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e"
TIMEOUT = 10

cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True

#options = webdriver.FirefoxOptions()
#options.log.level = "trace"
#options.headless = True

#fp = webdriver.FirefoxProfile(r'/home/m/ma/maxv/bears/geckodriver')
#driver = webdriver.Firefox(executable_path=fp)
driver = webdriver.Firefox(executable_path=r'./geckodriver', capabilities=cap)
#driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
#driver = webdriver.Firefox()

#options = Options()
#options.add_argument("start-maximized")
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def getCapacity() -> int:
    try:
        driver.get(URL)
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'span'))
        WebDriverWait(driver, TIMEOUT).until(element_present)
        value = driver.find_element_by_css_selector(
            "#root > div > div > div.styles_main__3Ul1n.styles_sidebarOpen__1t7th > div.styles_waitTimeFullnessWrapper__3PRdQ > div > span"
        ).text
        # print(value)
        value = int(value.split("%")[0])
        return value
    except Exception as e:
        print(f"Error: {e}")
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
    # print(f"Adding entry: {content}")
    sheet.append_row(content)


########
# Loop #
########

INTERVAL = 60 * 5

# while True:
# TODO 'sleep' during closed hours (don't log)
cap = getCapacity()
if cap > 0:
    append([str(datetime.datetime.now()), cap])
# time.sleep(INTERVAL - time.time() % INTERVAL)
