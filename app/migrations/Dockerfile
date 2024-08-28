FROM python:3.12-slim

WORKDIR /app

ENV CLEAN_ENV=PROD

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY entities entities/
COPY configs configs/
COPY usecases usecases/
COPY infra infra/
COPY migrations migrations/

COPY alembic.ini .

CMD ["alembic", "upgrade", "head"]