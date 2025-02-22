FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]
