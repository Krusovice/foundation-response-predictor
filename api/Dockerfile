FROM python:3.12-slim

WORKDIR /app

COPY api_server.py ./
COPY ../src ./
COPY ../model_exports/linear_model/linear_model_latest.pkl ./linear_model_latest.pkl

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8100"]
