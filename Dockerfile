FROM rasa/rasa:2.8.0
WORKDIR '/app'
COPY . /app
USER root

COPY ./data /app/data

ADD config.yml config.yml
ADD credentials.yml credentials.yml
ADD domain.yml domain.yml
ADD endpoints.yml endpoints.yml

RUN  rasa train
VOLUME /app
VOLUME /app/data
VOLUME /app/models



CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]