# Stage 1
FROM python:3.10-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    pipenv requirements > requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2
FROM python:3.10-alpine

WORKDIR /app

COPY --from=builder  /app/wheels /wheels
COPY --from=builder  /app/requirements.txt .
COPY . /app

RUN pip install --no-cache /wheels/*
