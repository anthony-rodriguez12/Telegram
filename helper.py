import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from cfg import GDRIVE_SHEET_KEY

ITEM_SHEET = 'Vuelos'
CLIENT_SHEET = 'Asientos'

CREDS_JSON = 'access-key.json'


class gsheet_helper:
    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]