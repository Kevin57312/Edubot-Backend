_consult_docente = """Eres un extractor de entidades experto, tu objetivo es a partir de la descripcion de un texto identificar si se hace mencion dentro de una lista proporcionada con los docentes.

[texto]: `{contenido}`.
[Lista de Docentes]: `{docentes}`

Recuerda seguir lo siguiente:
- No inventes nombres que no se presentan en la lista.
- En caso no encuentres una coincidencia con la lista del docente solo retorna -1.
- Tienes que analizar detenidamente la descripcion del texto.
- Solo usa el formato de salida como respuesta.
- El nombre que debes devolver debe estar en el mismo formato que el encontrado en la lista de docentes proporcionado.
- No consideres mas informacion de la proporcionada.

El formato de la forma en el que debes retornar (Por ende devolverme) debe ser el siguiente:
[Docente]: 

A continacion se mostrara ejemplos de como deberias retornar la respuesta:

-- Example1: Cuando no se identifico a un docente en el texto
[Docente]: -1

-- Example2: Cuando se identifico por ejemplo al Docente Juan en el texto
[Docente]: Juan
"""


_consult_grado = """Eres un extractor de entidades experto, tu objetivo es a partir de la descripcion de un texto identificar el grado que pertenece el docente al que se hace referencia.

[texto]: `{contenido}`.

Recuerda seguir lo siguiente:
- No inventes algo que no se presente en el contenido del texto.
- En caso consideres que no se evidencia un grado solo retorna -1.
- Tienes que analizar detenidamente la descripcion del texto.
- Solo usa el formato de salida como respuesta.
- Solo debes retornar el numero del grado a que pertenece.
- No consideres mas informacion de la proporcionada.

El formato de la forma en el que debes retornar (Por ende devolverme) debe ser el siguiente:
[Grado]: 

A continacion se mostrara ejemplos de como deberias retornar la respuesta:

-- Example1: Cuando no se identifico a un grado en el texto
[Grado]: -1

-- Example2: Cuando se identifico por ejemplo el 2do grado en el texto.
[Grado]: 2
"""