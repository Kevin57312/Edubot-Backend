
import pandas as pd
from googleapiclient.http import MediaIoBaseDownload
import io
from PyPDF2 import PdfReader


def get_pdf_ids(service, folder_id, doc_prefix):
    query = f"'{folder_id}' in parents and mimeType='application/pdf'"
    files = service.files().list(q=query, fields='files(id, name)').execute()
    pdf_ids = []
    for file in files.get('files', []):
        if file.get('name').startswith(doc_prefix):
            pdf_ids.append(file.get('id'))
    return pdf_ids if pdf_ids else None

def read_pdf_content(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)
    reader = PdfReader(fh)
    content = ""
    for page_num in range(len(reader.pages)):
        content += reader.pages[page_num].extract_text()
    return content