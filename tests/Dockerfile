FROM python:latest
RUN apt update && \
    apt install -y netcat-openbsd

COPY . tests
WORKDIR /tests
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt 
    