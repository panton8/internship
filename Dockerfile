# Stage 1
FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./Pipfile ./Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --deploy --system  && \
    pipenv requirements > requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder  /app/wheels /wheels
COPY --from=builder  /app/requirements.txt .
COPY . .
RUN chmod +x ./entrypoint-django.sh

RUN pip install --no-cache /wheels/*

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#ENTRYPOINT ["/bin/bash", "/app/entrypoint-django.sh"]
