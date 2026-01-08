FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry 
RUN poetry config virtualenvs.create false 
RUN poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "cd src && poetry run alembic upgrade head &&  poetry run python main.py"]