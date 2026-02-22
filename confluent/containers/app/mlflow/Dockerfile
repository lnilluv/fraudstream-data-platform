FROM python:3.10-slim

COPY requirements.txt /tmp
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && pip install --no-cache-dir -r /tmp/requirements.txt
