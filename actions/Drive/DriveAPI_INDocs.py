import pandas as pd
from googleapiclient.http import MediaIoBaseDownload
import io

# Función para obtener el ID de la carpeta de Google Drive
def get_folder_id(service, folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields='files(id, name)').execute()
    folders = results.get('files', [])
    if folders:
        return folders[0].get('id')
    return None


# Función para obtener el ID del archivo de Google Sheets
def get_sheet_id(service, folder_id, sheet_name):
    files = service.files().list(q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'", fields='files(id, name)').execute()
    for file in files.get('files', []):
        if file.get('name') == sheet_name:
            return file.get('id')
    return None

# Función para leer el contenido de Google Sheets
def read_google_sheet(service, sheet_id):
    request = service.files().export_media(fileId=sheet_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    with io.BytesIO() as io_bytes:
        downloader = MediaIoBaseDownload(io_bytes, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        io_bytes.seek(0)
        # Leer el archivo de Google Sheets en un DataFrame de Pandas
        df = pd.read_excel(io_bytes)
    return df

def get_doc_id(service, folder_id, doc_name):
    files = service.files().list(q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.document'", fields='files(id, name)').execute()
    for file in files.get('files', []):
        if file.get('name') == doc_name:
            return file.get('id')
    return None

def read_google_doc(service, doc_id):
    request = service.files().export_media(fileId=doc_id, mimeType='text/plain')
    with io.BytesIO() as io_bytes:
        downloader = MediaIoBaseDownload(io_bytes, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        io_bytes.seek(0)
        # Leer el archivo de Google Docs y almacenarlo como una cadena de texto
        doc_content = io_bytes.read().decode('utf-8')
    return doc_content


def list_subfolders(service, folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields='files(id, name)').execute()
    subfolders = [folder.get('name') for folder in results.get('files', [])]
    return subfolders


def create_folder(service, folder_name, parent_folder_id=None):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]
    
    folder = service.files().create(body=file_metadata, fields='id').execute()
    print(f'Folder ID: {folder.get("id")}')
    return folder.get('id')

def copy_file_to_folder(service, file_id, folder_id, new_name):
    copied_file = {
        'name': new_name,
        'parents': [folder_id]
    }
    copied_file = service.files().copy(fileId=file_id, body=copied_file).execute()
    print(f'Copied File ID: {copied_file.get("id")}')
    return copied_file.get('id')

def find_file_in_folder(service, folder_id, file_name):
    query = f"'{folder_id}' in parents and name='{file_name}' and trashed=false"
    results = service.files().list(q=query, fields='files(id, name)').execute()
    items = results.get('id', [])
    return items