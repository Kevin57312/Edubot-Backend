from actions.Drive.Google import Create_Service
from actions.Drive.DriveAPI_INDocs import copy_file_to_folder, create_folder, find_file_in_folder, get_folder_id, get_sheet_id
from actions.Drive.DriveAPI_GPSheet import getValueCell, setValueCell

CREDENTIAL_FILE = './actions/Drive/credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
DRIVE_SERVICE = Create_Service(CREDENTIAL_FILE,API_NAME,API_VERSION, SCOPES)


def assign_scores(file_name, data, folder_name = None):
    spreadsheet_name = 'Plantilla_Monitoreo'
    mainfolder_name = "Fichas_Monitoreo"
    mainfolder_id = get_folder_id(DRIVE_SERVICE, mainfolder_name)
    spreadsheet_file_id = get_sheet_id(DRIVE_SERVICE, mainfolder_id, spreadsheet_name)
    
    if folder_name:
        sub_folder_id = create_folder(DRIVE_SERVICE, folder_name, mainfolder_id)
    else:
        sub_folder_id = get_folder_id(DRIVE_SERVICE, folder_name)

    file_id = find_file_in_folder(DRIVE_SERVICE,sub_folder_id, "nuevo_cambio_4G5")

    if not file_id:
        file_id = copy_file_to_folder(DRIVE_SERVICE, spreadsheet_file_id, sub_folder_id, file_name)
        
    setValueCell(data, file_id)


data = [
    {
        "range": "pc!k16",
        "values": [["Numero"]]
    }
]
a = getValueCell("PS!A5:A8", "16z_gI3_MEjBe5XZK8bT61f5U_hN4GWiL1Sw-1qDADaY")
print(a)
#assign_scores("test", data, folder_name = "Prueba")

#data = [
#    {
#        "range": "sheet1!B2",
#        "values": [["Numero"]]
#    },
#    {
#        "range": "sheet1!C2",
#        "values": [["Apurar"]]
#    },
#]
