FROM python:3.4-alpine

RUN apk add --no-cache make git

ADD requirements.txt /tmp/requirements.txt

RUN pip install --upgrade setuptools && \
	pip install -r /tmp/requirements.txt
