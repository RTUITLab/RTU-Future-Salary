FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/salary

COPY . .