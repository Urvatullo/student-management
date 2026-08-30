FROM python:3.13

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --default-timeout=1000 --retries=10 fastapi uvicorn sqlalchemy psycopg

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]