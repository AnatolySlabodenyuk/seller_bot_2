FROM python:3.12-slim-bullseye

WORKDIR /app

COPY fonts /app/fonts
COPY src /app
COPY requirements.txt /

RUN pip install -r /requirements.txt

CMD ["python", "main.py"]