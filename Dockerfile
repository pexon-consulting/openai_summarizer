FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt *.py /app/
COPY client_modules/ /app/client_modules/

RUN pip install --no-cache-dir -r requirements.txt

CMD ./main.py



