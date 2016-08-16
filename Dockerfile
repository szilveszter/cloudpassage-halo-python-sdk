FROM ubuntu:16.04
MAINTAINER toolbox@cloudpassage.com

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install \
    python-pip

COPY ./ /source/

RUN cd /source/cloudpassage && \
    pip install -r requirements.txt && \
    pip install pytest && \
    pip install .

WORKDIR /source/cloudpassage/tests

CMD py.test style unit
