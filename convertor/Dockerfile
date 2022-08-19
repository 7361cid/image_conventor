FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . .
RUN pip install poetry
COPY pyproject.toml ./pyproject.toml
RUN poetry install
EXPOSE  8000
CMD ["poetry", "run", "python", "/app/manage.py", "makemigrations"]
CMD ["poetry", "run", "python", "/app/manage.py", "migrate"]
