FROM python:3.10.9-slim-buster

RUN apt-get update && \
    apt-get install -y gcc libpq-dev postgresql-client && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

WORKDIR /app

COPY ./src/requirements.txt/ ./src/requirements.txt

RUN pip install -U pip && \
    pip install --no-cache-dir -r ./src/requirements.txt

COPY . .

CMD ["./src/entrypoint.sh"]