FROM python:latest

WORKDIR /app

RUN apt-get update && apt-get install -y cron vim supervisor

COPY requirements.txt automation.py /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN touch crontab /etc/cron.d/my-cron

RUN chmod 0644 /etc/cron.d/my-cron

RUN mkdir /var/log/cron

RUN mkdir /app/log
RUN touch /app/log/script.log

RUN mkdir -p /etc/supervisor/conf.d

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV CRON_SCHEDULE='0 9-17 * * *'
ENV confluence_username=
ENV confluence_token=
ENV openai_key=
ENV slack_token=
ENV slack_channel=

RUN echo "${CRON_SCHEDULE} root python /app/automation.py >> /var/log/cron/cron.log 2>&1" > /etc/cron.d/my-cron

CMD ["/usr/bin/supervisord"]
