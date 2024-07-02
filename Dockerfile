FROM python:3.10.11

# Copia todo el contenido del directorio actual al contenedor
COPY ./data /app/data
COPY domain.yml /app/domain.yml
COPY credentials.yml /app/credentials.yml
COPY config.yml /app/config.yml
COPY domain.yml /app/domain.yml
COPY endpoints.yml /app/endpoints.yml
COPY requirements.txt /app/requirements.txt
COPY ./actions/__init__.py /app/actions/__init__.py
COPY ./actions/actions.py /app/actions/actions.py

RUN mkdir /app/models


# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala las dependencias de Python
RUN pip install -r requirements.txt

RUN rasa train

# Expone el puerto 5005 para el servidor de Rasa
EXPOSE 5005

# Comando para ejecutar el servidor de Rasa con las acciones personalizadas
CMD ["rasa", "run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]