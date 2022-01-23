from typing import List
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

import scraper

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


def append(content: List):
    print(f"Adding entry: {content}")
    sheet.append_row(content)


append([str(datetime.datetime.now()), scraper.getCapacity()])
