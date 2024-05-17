FROM python:3.11.4-slim-buster

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

EXPOSE $PORT

CMD python manage.py migrate & python manage.py runserver 0.0.0.0:$PORT
