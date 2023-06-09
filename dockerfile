FROM python:latest

WORKDIR /app

RUN apt-get update && apt-get install -y cron vim

COPY requirements.txt automation.py /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN touch crontab /etc/cron.d/my-cron

RUN chmod 0644 /etc/cron.d/my-cron

RUN mkdir /var/log/cron

RUN mkdir ./log
RUN touch ./log/script.log

ENV CRON_SCHEDULE='0 9-17 * * *'
ENV confluence_username=
ENV confluence_token=
ENV openai_key=
ENV slack_token=
ENV slack_channel=

RUN echo "${CRON_SCHEDULE} root python ./automation.py >> /var/log/cron/cron.log 2>&1" > /etc/cron.d/my-cron

CMD cron && tail -f ./log/script.log


