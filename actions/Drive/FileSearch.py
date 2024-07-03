from actions.Drive.DriveAPI_GPDocs import get_pdf_ids, read_pdf_content
from actions.Drive.DriveAPI_INDocs import get_folder_id, get_sheet_id, list_subfolders, read_google_sheet
from datetime import datetime
import pandas as pd

from actions.Drive.Google import Create_Service

CREDENTIAL_FILE = './actions/Drive/credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

DRIVE_SERVICE = Create_Service(CREDENTIAL_FILE,API_NAME,API_VERSION, SCOPES )

def Relacion_Docentes():    
    folder_name = 'Pruebas_chatbot'
    sheet_name = 'Relacion_Docentes'

    # Obtener el ID de la carpeta
    folder_id = get_folder_id(DRIVE_SERVICE, folder_name)

    if folder_id:
        # Obtener el ID del archivo de Google Sheets
        sheet_id = get_sheet_id(DRIVE_SERVICE, folder_id, sheet_name)
        if sheet_id:
            # Leer el contenido del archivo de Google Sheets
            existing_df = read_google_sheet(DRIVE_SERVICE, sheet_id)
            return existing_df
        else:
            print(f"No se encontró el archivo '{sheet_name}' en la carpeta '{folder_name}'.")
    else:
        print(f"No se encontró la carpeta '{folder_name}'.")


def Relacion_Semanas():    
    folder_name = 'Pruebas_chatbot'
    sheet_name = 'Relacion_Semanas'

    # Obtener el ID de la carpeta
    folder_id = get_folder_id(DRIVE_SERVICE, folder_name)

    if folder_id:
        # Obtener el ID del archivo de Google Sheets
        sheet_id = get_sheet_id(DRIVE_SERVICE, folder_id, sheet_name)
        if sheet_id:
            # Leer el contenido del archivo de Google Sheets
            existing_df = read_google_sheet(DRIVE_SERVICE, sheet_id)
            return existing_df
        else:
            print(f"No se encontró el archivo '{sheet_name}' en la carpeta '{folder_name}'.")
    else:
        print(f"No se encontró la carpeta '{folder_name}'.")

def Buscar_docs_Gestion(tipo_gestion):
    dict_tg = {
        "unidades de aprendizaje": "UA", 
        "sesiones de aprendizaje": "SA",
        "planificacion anual": "PA"
    } 
    prefix_doc = dict_tg[tipo_gestion]

    df = Relacion_Semanas()
    df["Rango inicial"] = pd.to_datetime(df["Rango inicial"], format="%d/%m/%Y")
    df["Rango final"] = pd.to_datetime(df["Rango final"], format="%d/%m/%Y")
    fecha_actual = datetime.now()

    periodo_actual = df[(df["Rango inicial"] <= fecha_actual) & (df["Rango final"] >= fecha_actual)]

    if periodo_actual.empty:
        periodo_actual = df[df["Rango final"] < fecha_actual].iloc[-1]
    else:
        periodo_actual = periodo_actual.iloc[0]

    if(prefix_doc == "UA"):
        unidad = periodo_actual["Unidad"]
        return f'{prefix_doc}{unidad}'
        
    if(prefix_doc == "SA"):
        bimestre = periodo_actual["Bimestre"]
        semana = periodo_actual["Semana"]
        return f'{prefix_doc}_B{bimestre}_S{semana}'

    return f'{prefix_doc}'


def indentificar_folder(curso, main_folder_id):
    if curso is not None:
        return [curso]
    
    folders_final = list_subfolders(DRIVE_SERVICE, main_folder_id)
    return folders_final


def Buscar_Tipo_Gestion(tipo_gestion, curso = None):

    main_folder_name = tipo_gestion
    main_folder_id = get_folder_id(DRIVE_SERVICE, main_folder_name)

    docs = Buscar_docs_Gestion(tipo_gestion)
    
    folders = indentificar_folder(curso, main_folder_id)
    dict_final = {}

    for folder in folders:
        contents = list()

        folder_id = get_folder_id(DRIVE_SERVICE, folder, parent_id=main_folder_id)
        docs_ids = get_pdf_ids(DRIVE_SERVICE, folder_id, docs)

        if docs_ids:
            for docs_id in docs_ids:
                content = read_pdf_content(DRIVE_SERVICE, docs_id)
                contents.append(content)

            dict_final[folder] = contents
            
    return dict_final