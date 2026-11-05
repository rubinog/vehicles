FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY static static
ENV DB_PATH=/data/vehicles.db
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "1", "app:app"]
