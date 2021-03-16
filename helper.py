import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from cfg import GDRIVE_SHEET_KEY

ITEM_SHEET = 'Vuelos'
CLIENT_SHEET = 'Lista'
TIKET_SHEET = 'Asientos'

CREDS_JSON = 'access-key.json'


class gsheet_helper:
    def __init__(self):
        scopes = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            CREDS_JSON,
            scopes
        )

        self.client = gspread.authorize(creds)
        self.gsheet = self.client.open_by_key(GDRIVE_SHEET_KEY)


    def getlistado(self):
        sheetPart = self.gsheet.worksheet(ITEM_SHEET)
        Parte = pd.DataFrame(sheetPart.get('A1:B11'))
        sheetComp = self.gsheet.worksheet(CLIENT_SHEET)
        Completo = pd.DataFrame(sheetComp.get_all_records(),index=['','','','','','',''])
        #Vuelos = pd.DataFrame(sheet.get('A4:B14'))
        #p = pd.DataFrame(sheet.get('A1:K2'))
        return Completo

    def store_user(self, New_Avi):
        
        print(New_Avi)
        sheet = self.gsheet.worksheet(CLIENT_SHEET)
        items = pd.DataFrame(sheet.get_all_records(),index=['','','','','','',''])

        lista = pd.DataFrame(items)
        cond = lista[lista["Aerop - Origen:"] == New_Avi].empty
        
        if cond:
            print("El aeropuerto NO esta registrado")
        else:
            print("El aeropuerto si existe y es el: %s",New_Avi)

        #sheet = self.gsheet.worksheet(CLIENT_SHEET)
        #sheet.add_rows(1)
        #sheet.append_row([element for element in New_Avi.values()])

if __name__ == "__main__":
    print(gsheet_helper().getlistado())
    