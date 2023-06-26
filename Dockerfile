FROM python:3.11

WORKDIR /app

COPY requirements.txt summarize_blogposts.py /app/
COPY client_modules/ /app/client_modules/

RUN pip install --no-cache-dir -r requirements.txt

CMD ./summarize_blogposts.py



