# Build Stage
FROM python:3.14-slim AS builder
WORKDIR /my_app
COPY requirements.txt .
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Run Stage
FROM python:3.14-slim
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"    
WORKDIR /my_app
COPY --from=builder /venv /venv
COPY . .
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]
