FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files first so Docker can cache this layer
COPY pyproject.toml poetry.lock* ./

# Install dependencies (no virtualenv needed inside a container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy application source
COPY main.py .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
