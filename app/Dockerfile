FROM python:3.12-slim

WORKDIR /app

ENV CLEAN_ENV=PROD

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY entities entities/
COPY configs configs/
COPY usecases usecases/
COPY rest rest/
COPY infra infra/

COPY entry.py .

EXPOSE 8090

CMD ["uvicorn", "entry:app", "--port", "8090", "--host", "0.0.0.0"]