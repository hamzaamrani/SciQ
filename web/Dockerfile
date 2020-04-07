FROM python:3.7

RUN apt update && \
    apt install -y netcat-openbsd

EXPOSE 5000

WORKDIR /usr/src/sciq

ADD ./web/requirements.txt .

RUN pip3 install -r requirements.txt 

COPY ./web/docker-entrypoint.sh .
COPY ./web/run.py .
COPY ./web/.env .
COPY ./tests tests
COPY ./web/migrations migrations
ADD ./web/app app

CMD ["/bin/bash", "/usr/src/sciq/docker-entrypoint.sh"]


