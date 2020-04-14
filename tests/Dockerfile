FROM docker:latest
RUN apk update
RUN apk add python3
RUN apk add py3-pip
RUN apk add git
RUN apk add build-base python3-dev jpeg-dev zlib-dev
COPY . tests
WORKDIR /tests
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt 
    