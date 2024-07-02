FROM rasa/rasa:3.7.0a1-full

# Copia todo el contenido del directorio actual al contenedor
COPY ./data /app/data
COPY domain.yml /app/domain.yml
COPY credentials.yml /app/credentials.yml
COPY config.yml /app/config.yml
COPY domain.yml /app/domain.yml
COPY endpoints.yml /app/endpoints.yml
COPY ./actions/__init__.py /app/actions/__init__.py
COPY ./actions/actions.py /app/actions/actions.py

RUN mkdir /app/models
USER root

# Establece el directorio de trabajo en /app
WORKDIR /app

RUN rasa train

VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]