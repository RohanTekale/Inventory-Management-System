FROM python:3.10-slim

WORKDIR /app

# Install dependencies: git (for git+ URLs) and FreeTDS build deps
RUN apt-get update && \
    apt-get install -y git gcc g++ build-essential libssl-dev libffi-dev libpq-dev libxml2-dev libxslt1-dev zlib1g-dev libsybdb5 freetds-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "inventory_management.wsgi:application"]
