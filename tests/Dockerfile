FROM python:latest
RUN apt update
RUN apt install python3
RUN apt install py3-pip
RUN apt install git
RUN apt install build-base python3-dev jpeg-dev zlib-dev
COPY . tests
WORKDIR /tests
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt 
    