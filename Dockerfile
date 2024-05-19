FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . /app

CMD ["tail", "-f", "/dev/null"]
