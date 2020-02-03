FROM python:3.8-alpine as application
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN apk update && \
    apk add postgresql-dev \
            gcc \
            python3-dev \
            musl-dev

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt --no-cache-dir

COPY . .
