FROM python:3.12.3-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --upgrade poetry

RUN poetry install --no-root

COPY . /app/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
