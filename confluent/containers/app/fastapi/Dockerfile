FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY /app/fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/fastapi .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
