FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY models/ ./models/

ENV FLASK_HOST=0.0.0.0
ENV PORT=5001

EXPOSE 5001

CMD ["python", "app/api.py"]
