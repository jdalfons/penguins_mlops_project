FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install psycopg2-binary

COPY . .

COPY models /app/models

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

