FROM python:3.6

RUN apt update && \
    apt install -y netcat-openbsd

EXPOSE 5000

COPY . /sciq

WORKDIR /sciq

RUN pip3 install -r requirements.txt 

CMD ["/bin/bash", "/sciq/docker-entrypoint.sh"]
