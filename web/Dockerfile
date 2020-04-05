FROM python:3.7

RUN apt update && \
    apt install -y netcat-openbsd

EXPOSE 5000

WORKDIR /usr/src/sciq

ADD ./requirements.txt .

RUN pip3 install -r requirements.txt 

COPY docker-entrypoint.sh .
COPY run.py .
COPY .env .
COPY tests tests
COPY migrations migrations
ADD app app

CMD ["/bin/bash", "/usr/src/sciq/docker-entrypoint.sh"]


