import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from cfg import GDRIVE_SHEET_KEY

ITEM_SHEET = 'Vuelos'
CLIENT_SHEET = 'Lista'
TIKET_SHEET = 'Asientos'
FACTUR_SHEET = 'Factura'
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
        Completo = pd.DataFrame({"|ID|":sheetComp.get('A2:A27'),
                                 "|Avion|":sheetComp.get('B2:B27'),
                                 "|IATA|":sheetComp.get('C2:C27'),
                                 "|Pais-Origen|":sheetComp.get('D2:D27'),
                                 "|Pais-Destino|":sheetComp.get('E2:E27'),
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
            print(cell)
            print(f"Resultados del ID:{name}")
            Col1 = {
            'A1': "A1",
            'A2': "C1", 
            'A3': "E1",
            'A4': "G1",
            'A5': "I1", 
            'B1': "K1", 
            'C1': "M1",
            'C2': "O1",
            'C3': "Q1", 
            'C4': "S1",
            'D1': "U1",
            'D2': "W1", 
            'D3': "Y1", 
            'E1': "AA1",
            'E2': "AC1",
            'E3': "AE1",            
            'F1': "AG1", 
            'F2': "AI1",
            'F3': "AK1",
            'F4': "AM1", 
            'F5': "AO1", 
            'G1': "AQ1",
            'G2': "AS1",
            'G3': "AU1",
            'G4': "AW1", 
            'G5': "AY1", 
}
            Col2 = {
            'A1': "B11",   
            'A2': "D11", 
            'A3': "F11",
            'A4': "H11",
            'A5': "J11", 
            'B1': "L11", 
            'C1': "N11",
            'C2': "P11",
            'C3': "R11", 
            'C4': "T11",
            'D1': "V11",
            'D2': "X11", 
            'D3': "Z11", 
            'E1': "AB11",
            'E2': "AD11",
            'E3': "AF11",            
            'F1': "AH11", 
            'F2': "AJ11",
            'F3': "AL11",
            'F4': "AN11", 
            'F5': "AP11", 
            'G1': "AR11",
            'G2': "AT11",
            'G3': "AV11",
            'G4': "AX11", 
            'G5': "AZ11", 
}
            range = Col1.get(name)+':'+Col2.get(name)
        
            #val = sheetComp.cell(cell.row, cell.col).value  para conseguir el nombre de una CELL
            df = pd.DataFrame(sheetView.get(range),columns=['*** REGRISTRO DE ***', '*** DATOS ***'],index=['', '', '','','','','','','','',''])
        except:
            df = f"Losiento No hay ninguna ID con el nombre de: {name}"
        
        return df

    
    def Buscar_ID(self, New_Avi):
        
        sheet = self.gsheet.worksheet(CLIENT_SHEET)
        items = pd.DataFrame(sheet.get_all_records())
        items.index.name = 'Id'
        lista = pd.DataFrame(items)
        cond = lista[lista["|ID|"] == New_Avi].empty

        if cond:
            print("El ID NO existe")
            return "losiento"
        else:
            print(f"El ID:{New_Avi} si existe")
            return 'ok'

    def FechNube(self, Range): 
        try:
            Nube = self.gsheet.worksheet(FACTUR_SHEET)
            times = time.strftime("%d/%m/%y")
            Nube.update(Range , times)
            print(f"Esto es la celda: {Range}")
            
            return 'Se Guardo Bien '
        except:
            return 'Algo Fallo'


    def mostrar(self): 
        sheetView = self.gsheet.worksheet(FACTUR_SHEET)
        Reply = sheetView.get('D4').first()
        try:
            Reply = int(Reply)
        except:
            Reply = Reply
        if Reply == 1:
            df = pd.DataFrame(sheetView.get('A1:B9'),columns=['*** DETALLES ***', '*** DATOS ***'],index=['', '', '','','','','','',''])
            val = sheetView.get('B10').first()
            lista = [df,val,Reply]
        elif   Reply == 2:
            df = pd.DataFrame(sheetView.get('A14:B22'),columns=['*** DETALLES ***', '*** DATOS ***'],index=['', '', '','','','','','',''])
            val = sheetView.get('B10').first()
            lista = [df,val,Reply]
        else:
            lista = ['hubo un','Error']

        return lista


    def SaveNube(self, Range, text): 
        try:
            Nube = self.gsheet.worksheet(FACTUR_SHEET)
            Nube.update(Range , text)
            print(f"Esto es la celda: {Range}")
            print(f"Este es el contenido: {text}")
            return 'Se Guardo Bien '
        except:
            return 'Algo Fallo'
    
    def Retornar_ID(self):
        TheID = self.gsheet.worksheet(FACTUR_SHEET)
        Value = TheID.get('B1').first()
        
        return Value

    def Buscar_Asientos(self, ID):
        TheID = self.gsheet.worksheet(TIKET_SHEET)
        Cell = TheID.find(ID)
        row = Cell.row
        val = TheID.cell(row, 3).value

        return val


if __name__ == "__main__":
    #print(gsheet_helper().getlistado())
    #print(gsheet_helper().SaveNube('B1','Funciona'))
    print(gsheet_helper().mostrar())
    #print(gsheet_helper().store_user("Ecuador"))
    #print(gsheet_helper().Ver_Vuelo('A1'))
    
    