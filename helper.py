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
        sheetComp = self.gsheet.worksheet(CLIENT_SHEET)
        #sheetComp.get_all_records(CLIENT_SHEET) para traer todas las tablas
        #sheetPart.get('A1:B11')
        Completo = pd.DataFrame({"|ID|":sheetComp.get('A2:A8'),
                                 "|Avion|":sheetComp.get('B2:B8'),
                                 "|IATA|":sheetComp.get('C2:C8'),
                                 "|Pais-Origen|":sheetComp.get('D2:D8'),
                                 "|Pais-Destino|":sheetComp.get('E2:E8')
                                })
       
        return Completo

    def Buscar(self, name):
        sheetComp = self.gsheet.worksheet(CLIENT_SHEET) 
        cell_list = sheetComp.findall(name)
        x = len(cell_list)
        if x > 0:
            print(cell_list)
            
            #print(x)
            #print(f"Tenemos {x} Resultados:")
            L = []
            for indice in cell_list:
                cell = indice   
                values_list = sheetComp.row_values(cell.row)
                L.append(values_list)
            #val = sheetComp.cell(cell.row, cell.col).value  para conseguir el nombre de una CELL
            df = pd.DataFrame(L, columns=['|ID|','Avion|','IATA|','Pais-Origen|','Pais-Des|','Aerop - Origen|','Aerop - Destino|'])
        else:
            df = "Losiento No hay Coincidencias"
        
        return df

    def Ver_Vuelo(self, name): 
        sheetView = self.gsheet.worksheet(ITEM_SHEET)
        try:
            cell = sheetView.find(name)
            
            print(f"Resultados del ID:{name}")
            Col1 = {
            'A1': "A1",'B1': "C1", 'C1': "E1",'D1': "G1",
            'E1': "I1", 'F1': "K1", 'G1': "M1"}
            Col2 ={
            'A1': "B11", 'B1': "D11",  'C1': "F11",
            'D1': "H11",'E1': "J11", 'F1': "L11", 'G1': "N11"}
            range = Col1.get(name)+':'+Col2.get(name)
        
            #val = sheetComp.cell(cell.row, cell.col).value  para conseguir el nombre de una CELL
            df = pd.DataFrame(sheetView.get(range))
        except:
            df = f"Losiento No hay ninguna ID con el nombre de: {name}"
        
        return df


    def store_user(self, New_Avi):
        
        sheet = self.gsheet.worksheet(CLIENT_SHEET)
        items = pd.DataFrame(sheet.get_all_records(),index=['','','','','','',])
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
    #print(gsheet_helper().getlistado())
    print(gsheet_helper().Ver_Vuelo("tony"))
    #print(gsheet_helper().store_user("Ecuador"))
    #print(gsheet_helper().Ver_Vuelo('A1'))
    