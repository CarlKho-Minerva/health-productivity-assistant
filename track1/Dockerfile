FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY health_agent/ ./health_agent/
COPY health_vault/ ./health_vault/
COPY app.py .
COPY static/ ./static/
ENV PORT=8080
CMD ["python", "app.py"]
