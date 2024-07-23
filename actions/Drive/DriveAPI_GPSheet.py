from actions.Drive.Google import Create_Service

CREDENTIAL_FILE = './actions/Drive/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
API_NAME = 'sheets'
API_VERSION = 'v4'
service = Create_Service(CREDENTIAL_FILE,API_NAME,API_VERSION, SCOPES)

def setValueCell(data, spreadsheet_id):
    body = {
        "valueInputOption": "RAW",
        "data": data
    }
    sheet = service.spreadsheets()
    request = sheet.values().batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    response = request.execute()

    print(f"{response.get('updatedCells')} celdas actualizadas.")
    print(response)

    return


def getValueCell(range, spreadsheet_id):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    values = result.get('values', [])
    if not values:
        return None    
    return values


def shift_right(cell, n):
    column = ''.join([char for char in cell if char.isalpha()])
    row = ''.join([char for char in cell if char.isdigit()])

    def column_to_number(col):
        number = 0
        for char in col:
            number = number * 26 + (ord(char.upper()) - ord('A')) + 1
        return number

    def number_to_column(num):
        column = ''
        while num > 0:
            num, remainder = divmod(num - 1, 26)
            column = chr(remainder + ord('A')) + column
        return column

    number_column = column_to_number(column)
    new_column = number_to_column(number_column + n)

    return f'{new_column}{row}'


def increase_range(range_str):
    letter_part = ''.join(filter(str.isalpha, range_str))
    numeric_part = ''.join(filter(str.isdigit, range_str))
    
    new_numeric_part = int(numeric_part) + 1
    new_range = f'{letter_part}{new_numeric_part}'
    
    return new_range