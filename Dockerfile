FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY itfox/ /app

WORKDIR /app

CMD ["gunicorn", "itfox.wsgi:application", "--bind", "0:8000" ]