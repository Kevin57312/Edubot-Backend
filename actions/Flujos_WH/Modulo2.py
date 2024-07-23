from datetime import datetime
from actions.Drive.FileSearch import Relacion_Docentes
from actions.llm.llama.Gestion_Educativa.llm_gestion import search_docente
from actions.Drive.Google import Create_Service
from actions.Drive.DriveAPI_INDocs import copy_file_to_folder, create_folder, find_file_in_folder, get_folder_id, get_sheet_id
from actions.Drive.DriveAPI_GPSheet import getValueCell, increase_range, setValueCell, shift_right

CREDENTIAL_FILE = './actions/Drive/credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
DRIVE_SERVICE = Create_Service(CREDENTIAL_FILE,API_NAME,API_VERSION, SCOPES)

def validar_docente(mensaje):
    datos = Relacion_Docentes()
    docentes = set(datos['APELLIDOS Y NOMBRES'])
    docente = search_docente(mensaje, docentes)
    return docente


def validate_folder(folder_name):
    mainfolder_name = "Fichas_Monitoreo"
    mainfolder_id = get_folder_id(DRIVE_SERVICE, mainfolder_name)
    folder_id = get_folder_id(DRIVE_SERVICE, folder_name, parent_id=mainfolder_id)

    if not folder_id:
        create_folder(DRIVE_SERVICE, folder_name, mainfolder_id)
    return


def get_final_evl_by_cat(category, score, spreadsheet_file_id):
    dict_ranges = {
        "pc": "PS!A5:A8",
        "cm": "PS!F5:F8",
        "re": "PS!M5:M8"
    }

    grados = getValueCell(dict_ranges[category],spreadsheet_file_id)

    for item in grados:
        grade, limits = item[0].split(': ')
        lower_limit, upper_limit = map(int, limits.split('-'))
        if lower_limit <= score <= upper_limit:
            return grade
    return "Number out of range"


def obtener_fecha_formateada():
    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime('%d_%m_%Y')
    return fecha_formateada

def fill_initial_data(gradoysec, docente, date, sesion):

    datos = Relacion_Docentes()
    filter_docente = datos[datos['APELLIDOS Y NOMBRES'] == docente].index
    course = datos.loc[filter_docente[0], 'Curso']

    data = [
        {
            "range": "pc!d6",
            "values": [[docente]]
        },
        {
            "range": "pc!d7",
            "values": [[sesion]]
        },
        {
            "range": "pc!d8",
            "values": [[course]]
        },
        {
            "range": "pc!d9",
            "values": [[date]]
        },
        {
            "range": "pc!v6",
            "values": [[gradoysec]]
        },
    ]

    return data


def assign_scores_in_sheet(total_dict,len_preguntas, labels):
    gradoysec = total_dict["gradoysec"]
    docente = total_dict["docente"]
    sesion = total_dict["sesion"]
    date = obtener_fecha_formateada()

    data = fill_initial_data(gradoysec, docente, date, sesion)
    
    # Estan evaluadas de acuerdo a los tres labels [pc, cm, re]
    mark_cells = ["k16", "d4", "d18"]
    summary_cells = ["c3", "i3", "o3"]
    sheet_names = ["pc","ft","ft"]

    spreadsheet_name = 'Plantilla_Monitoreo'
    mainfolder_name = "Fichas_Monitoreo"
    mainfolder_id = get_folder_id(DRIVE_SERVICE, mainfolder_name)
    spreadsheet_file_id = get_sheet_id(DRIVE_SERVICE, mainfolder_id, spreadsheet_name)
    
    file_name = f"Evaluacion_{gradoysec}_{date}"
    j = 0

    for len in len_preguntas:
        label = labels[j]
        mark_cell = mark_cells[j]
        values = total_dict[label]
        sum_values = 0
        sheet_name = sheet_names[j]
        for i in range(len):
            score = int(values[i])
            dict_value = dict()

            if score>1:
                tmp_mark_cell = shift_right(mark_cell,score-1)
                dict_value['range']= f"{sheet_name}!{tmp_mark_cell}"
            else:
                dict_value['range']= f"{sheet_name}!{mark_cell}"

            dict_value['values']= [["X"]]

            mark_cell = increase_range(mark_cell)
            sum_values += score
            data.append(dict_value)

        dict_value = dict()
        summary_value = get_final_evl_by_cat(label, sum_values,spreadsheet_file_id)
        dict_value['range']= f"ps!{summary_cells[j]}"
        dict_value['values']= [[f"{summary_value}:{sum_values}"]]
        data.append(dict_value)

        j +=1

    send_scores_to_sheet(file_name, data, docente, spreadsheet_file_id)

    return True

def send_scores_to_sheet(file_name, data, folder_name, spreadsheet_file_id):
    
    sub_folder_id = get_folder_id(DRIVE_SERVICE, folder_name)
    
    file_id = get_sheet_id(DRIVE_SERVICE,sub_folder_id, file_name)
    
    if not file_id:
        file_id = copy_file_to_folder(DRIVE_SERVICE, spreadsheet_file_id, sub_folder_id, file_name)
        
    setValueCell(data, file_id)

    return