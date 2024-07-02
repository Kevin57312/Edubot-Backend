FROM rasa/rasa:3.1.0
WORKDIR '/app'
COPY . /app
USER root

COPY ./data /app/data

ADD config.yml /app/config.yml
ADD credentials.yml /app/credentials.yml
ADD domain.yml /app/domain.yml
ADD endpoints.yml /app/endpoints.yml

RUN  rasa train
VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]