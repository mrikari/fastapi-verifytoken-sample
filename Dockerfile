FROM python:3.11-alpine

COPY ./src /var/opt/src
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

WORKDIR /var/opt/src

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
