FROM ubuntu:16.04
MAINTAINER toolbox@cloudpassage.com

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    python-pip

COPY ./ /source/

WORKDIR /source/

RUN pip install -r requirements.txt && \
    pip install pytest && \
    pip install mock && \
    pip install .

WORKDIR /source/tests

CMD py.test style unit
