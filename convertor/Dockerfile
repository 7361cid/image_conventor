FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD ./app
RUN pip install poetry
RUN poetry install
