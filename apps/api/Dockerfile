FROM python:9.99-slim AS builder
ENV PYTHONUNBUFFERED=1
RUN useradd -m appuser
WORKDIR /my_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
CMD ["python", "app.py"]