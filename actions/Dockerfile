FROM rasa/rasa-sdk:3.6.2

WORKDIR /app

COPY requirements.txt requirements.txt 

USER root

RUN pip3 install --verbose -r requirements.txt

EXPOSE 5055

USER 1001