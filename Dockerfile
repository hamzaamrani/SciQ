FROM python:3.6

RUN apt update && \
    apt install -y netcat-openbsd

EXPOSE 5000

ADD requirements.txt /sciq/requirements.txt

WORKDIR /sciq

RUN pip3 install -r requirements.txt 

COPY docker-entrypoint.sh /sciq/docker-entrypoint.sh
COPY run.py /sciq/run.py
COPY .env /sciq/.env
COPY /tests /sciq/tests
COPY /migrations /sciq/migrations
ADD /app /sciq/app

CMD ["/bin/bash", "/sciq/docker-entrypoint.sh"]


