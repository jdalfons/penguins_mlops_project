# filepath: /Users/halcolo/Documents/code/lyon2/MASTER 2/MLOPS/penguin_mlops_project/mlflow/Dockerfile
FROM python:3.11.10-slim

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5001"]