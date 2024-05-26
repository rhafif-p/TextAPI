# syntax=docker/dockerfile:1
FROM python:3.11
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
ENTRYPOINT ["gunicorn", "app:app", "-b", "0.0.0.0:8080"]
