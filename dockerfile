# Verwenden Sie das offizielle Python-Image von Docker Hub
FROM python:latest

WORKDIR /app

RUN apt-get update && apt-get install -y cron vim

COPY myscript.py /app/myscript.py

COPY setup_cron.sh /app/setup_cron.sh

RUN chmod +x /app/setup_cron.sh

RUN mkdir /logs

# Fügen Sie die Umgebungsvariablen hinzu
ENV CRON_SCHEDULE=0 9-17 * * *
ENV confluence_username=
ENV onfluence_token=
ENV openai_key=
ENV slack_token=
ENV slack_channel=

CMD ["/app/setup_cron.sh"]
