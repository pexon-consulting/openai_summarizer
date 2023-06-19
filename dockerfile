FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y

COPY requirements.txt automation.py /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ./log
RUN touch ./log/script.log

ENV Confluence_username=
ENV Confluence_token=
ENV Openai_api_key=
ENV Slack_token=
ENV Slack_channel=


CMD python ./automation.py


