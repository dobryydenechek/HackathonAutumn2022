FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
# ENV DOCKER_DEFAULTPLATFORM=linux/amd64

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
