FROM ubuntu:bionic

ADD . /mloc
WORKDIR /mloc

RUN apt-get update && \
    mkdir -p /data/db && \
    apt-get install -y python3-dev python3-pip mongodb git && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt --use-feature=2020-resolver

CMD service mongodb start && python3 -m mloc

EXPOSE 5000
