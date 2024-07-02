FROM rasa/rasa:3.6.18

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

VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]