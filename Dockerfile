FROM python:3.7-buster

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

WORKDIR /app
COPY powerdummy /app/powerdummy
COPY poetry.lock populate.py pyproject.toml /app/

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

ENV PYTHONPATH=/app
ENTRYPOINT ["python3","populate.py"]
