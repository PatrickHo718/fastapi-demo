FROM python:3.11-alpine3.20
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apk add musl-dev mariadb-connector-c-dev gcc
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
