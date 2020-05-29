FROM python:latest
RUN apt update
RUN apt install python3
RUN apk install py3-pip
RUN apk install git
RUN apk install build-base python3-dev jpeg-dev zlib-dev
COPY . tests
WORKDIR /tests
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt 
    