FROM python:3.12-slim

WORKDIR /app

COPY ./api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api/api_server.py ./
COPY ./src/ ./src/
COPY ./model_exports/linear_model/linear_model_latest.pkl ./models/

EXPOSE 8100

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8100"]
