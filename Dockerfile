FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /source
WORKDIR /source
ADD requirements.txt /source/
RUN pip install -r requirements.txt
ADD . /source/
