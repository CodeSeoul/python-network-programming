FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile ./
RUN pip install pipenv && pipenv install

RUN mkdir /src
WORKDIR /src
COPY ./src /src

RUN adduser -D user
USER user