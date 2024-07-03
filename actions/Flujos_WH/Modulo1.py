import os

from actions.Drive.FileSearch import DRIVE_SERVICE, Buscar_docs_Gestion, Relacion_Docentes, indentificar_folder
from actions.Drive.DriveAPI_GPDocs import get_pdf_ids, read_pdf_content
from actions.Drive.DriveAPI_INDocs import get_folder_id
from actions.llm.llama.Gestion_Educativa.llm_gestion import search_docente, search_grado


import smtplib
from email.mime.text import MIMEText

def transform_to_text(dict_cursos, dict_grados):
    final_text = []

    for key, value in dict_cursos.items():
        grados_faltantes = dict_grados.get(key, list(range(1, value[2]+1)))
        final_text.append(f"- Curso {key} \n\tDocente: {value[0]} \n\tGrados faltantes: {grados_faltantes}\n\n")
    return ''.join(final_text)


def Buscar_Tipo_Gestion_Docentes(tipo_gestion, curso=None):
    main_folder_name = tipo_gestion
    main_folder_id = get_folder_id(DRIVE_SERVICE, main_folder_name)


    docs = Buscar_docs_Gestion(tipo_gestion)
    folders = indentificar_folder(curso, main_folder_id)
    dict_final = {}
    dict_grados = {}

    datos = Relacion_Docentes()
    filter_datos = datos[datos['Lider'] == 1].copy()
    docentes = set(filter_datos['APELLIDOS Y NOMBRES'])

    for folder in folders:
        folder_id = get_folder_id(DRIVE_SERVICE, folder, parent_id=main_folder_id)
        docs_ids = get_pdf_ids(DRIVE_SERVICE, folder_id, docs)
        
        if docs_ids:
            set_grados = set()

            for docs_id in docs_ids:
                content = read_pdf_content(DRIVE_SERVICE, docs_id)[:580]
                grado = int(search_grado(content))
                set_grados.add(grado)

            docente = search_docente(content, docentes)

            filter_docente = datos[datos['APELLIDOS Y NOMBRES'] == docente].index
            grados_totales = datos.loc[filter_docente[0], 'Grados']

            if grados_totales == len(set_grados):
                filter_datos = filter_datos.drop(filter_docente)

            real_grados = set(range(1, grados_totales + 1))
            dict_grados[folder] = list(real_grados - set_grados)
        

    dict_final = {row['Curso']: [row['APELLIDOS Y NOMBRES'], row['Correo electronico'], row['Grados']] for _, row in filter_datos.iterrows()}
    
    return dict_final, dict_grados

def enviar_todos_correos(dict_cursos, dict_grados, tipo_gestion):
    for key, value in dict_cursos.items():
        grados_faltantes = dict_grados.get(key, list(range(1, value[2]+1)))
        enviar_correos(tipo_gestion, key, value[0], value[1], grados_faltantes)
    return 
    


def enviar_correos(tipo_gestion, curso, nombre_docente, to_email, grados):
    pws = os.environ["CONTRASENIA"] 
    from_email = os.environ["CORREO"]
    director = os.environ["DIRECTOR"]

    body = f"""Buenas tardes profesor {nombre_docente},

Hemos notado que aun no ha llegado a subir  {tipo_gestion} en el curso de {curso} para los grados {grados}, por favor subirlo lo antes posible. 
    
Atte. EduBot"""
    
    msg = MIMEText(body)

    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"[{curso}] Aviso de {tipo_gestion}"

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(from_email, pws)
            recipients = [to_email] + [director]
            smtp_server.sendmail(from_email, recipients, msg.as_string())
        
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")        

    return