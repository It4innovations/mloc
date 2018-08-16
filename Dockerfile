FROM ubuntu:bionic

ADD . /mloc
WORKDIR /mloc

RUN apt-get update && \
    mkdir -p /data/db && \
    apt-get install -y python3-dev python3-pip mongodb && \
    pip3 install -r requirements.txt

CMD service mongodb start && python3 mloc/mloc.py

EXPOSE 5000
