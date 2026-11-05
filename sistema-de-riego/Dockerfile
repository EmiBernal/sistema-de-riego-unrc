FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN tailwindcss --help

COPY . .
RUN tailwindcss -i app/static/src/input.css -o app/static/css/output.css --minify

CMD ["python", "run.py"]