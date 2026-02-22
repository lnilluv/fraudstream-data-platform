FROM python:3.10-slim

WORKDIR /home/app

COPY requirements.txt /dependencies/requirements.txt
RUN pip install --no-cache-dir -r /dependencies/requirements.txt

CMD ["bash"]
