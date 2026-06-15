FROM python:3.14-slim
WORKDIR /my_app
ENV PYTHONUNBUFFERED=1
COPY . .
RUN useradd -m appuser
USER appuser
CMD ["python", "worker.py"]