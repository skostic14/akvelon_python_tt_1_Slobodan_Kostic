FROM python:3.9.5-slim-buster

WORKDIR /app

COPY . main.py /app/

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]