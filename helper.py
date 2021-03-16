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
        #sheetComp.get_all_records(CLIENT_SHEET) para traer todas las tablas
        #sheetPart.get('A1:B11')
        Completo = pd.DataFrame({"|Avion|":sheetComp.get('A2:A8'),
                                 "|IATA|":sheetComp.get('B2:B8'),
                                 "|Pais-Origen|":sheetComp.get('C2:C8'),
                                 "|Pais-Destino|":sheetComp.get('D2:D8')
                                })
        Completo.index.name = 'Id'
       
        return Completo

    def Buscar(self):
        sheetComp = self.gsheet.worksheet(CLIENT_SHEET)
        name = "Canadá"
        #cell = sheetComp.find(name)
        cell_list = sheetComp.findall(name)
        x = len(cell_list)
        print(f"Tenemos {x} Resultados:")
        L = []
        for indice in cell_list:
            cell = indice   
            values_list = sheetComp.row_values(cell.row)
            L.append(values_list)
            
        #val = sheetComp.cell(cell.row, cell.col).value  para conseguir el nombre de una CELL
        df = pd.DataFrame(L, columns=['Id:','Avion:','Asientos-Libre:','Asient-Ocupa:'])
        print(df)

        


    def store_user(self, New_Avi):
        
        sheet = self.gsheet.worksheet(CLIENT_SHEET)
        items = pd.DataFrame(sheet.get_all_records())
        items.index.name = 'Id'
        lista = pd.DataFrame(items)
        cond = lista[lista["Pais-Origen|"] == New_Avi].empty
        
        if cond:
            print("El pais NO tiene vuelos actualmente")
        else:
            print(f"El si existen vuelos al pais:{New_Avi}")

        #sheet = self.gsheet.worksheet(CLIENT_SHEET)
        #sheet.add_rows(1)
        #sheet.append_row([element for element in New_Avi.values()])

if __name__ == "__main__":
    print(gsheet_helper().getlistado())
    print(gsheet_helper().Buscar())
    print(gsheet_helper().store_user("Ecuador"))
    