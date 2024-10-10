FROM python:3.9-slim

LABEL authors="shaygoldstein"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN pip install pymongo requests

WORKDIR /job

COPY . /job

ENTRYPOINT ["python", "/job/import_export_data.py"]