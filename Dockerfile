FROM python:3.11

WORKDIR /app

COPY requirements.txt summarize_blogposts.py client_modules/ /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD python ./summarize_blogposts.py



