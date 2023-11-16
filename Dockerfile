# Set base image (host OS)
FROM python:3.10-slim

# Set work directory in the container
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pipenv
RUN pip install pipenv

# Copy pip dependencies first, to take advantage of docker caching
COPY ./Pipfile ./Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install --deploy --system


# Copy the rest of the code
COPY . /app

# Copy the Django entrypoint script into the container
COPY entrypoint-django.sh /entrypoint-django.sh

# Give execution permissions to the entrypoint script
RUN chmod +x ./entrypoint-django.sh
