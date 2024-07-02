FROM rasa/rasa:3.6.20
WORKDIR '/app'
COPY . /app
USER root

COPY ./data /app/data

RUN  rasa train
VOLUME /app
VOLUME /app/data
VOLUME /app/models

EXPOSE 5005

CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug", "-p", "5005:5005"]