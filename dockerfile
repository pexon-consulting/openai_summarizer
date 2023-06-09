FROM python:latest

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Installieren Sie cron und vim (vim ist optional, aber nützlich für Debugging-Zwecke)
RUN apt-get update && apt-get install -y cron vim supervisor

# Kopieren Sie requirements.txt und Ihr Skript in den Container
COPY requirements.txt automation.py /app/

# Installieren Sie alle in requirements.txt aufgeführten Python-Pakete
RUN pip install --no-cache-dir -r requirements.txt

RUN touch crontab /etc/cron.d/my-cron

# Geben Sie der Crontab-Datei die richtigen Berechtigungen
RUN chmod 0644 /etc/cron.d/my-cron

# Erstellen Sie das Log-Verzeichnis
RUN mkdir /var/log/cron

RUN mkdir /app/log
RUN touch /app/log/script.log

RUN mkdir -p /etc/supervisor/conf.d

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Fügen Sie die Umgebungsvariablen hinzu
ENV CRON_SCHEDULE='0 9-17 * * *'
ENV confluence_username=
ENV confluence_token=
ENV openai_key=
ENV slack_token=
ENV slack_channel=

# Fügen Sie den Cron-Job hinzu (ersetzen Sie "my_script.py" durch den Namen Ihres Skripts)
RUN echo "${CRON_SCHEDULE} root python /app/automation.py >> /var/log/cron/cron.log 2>&1" > /etc/cron.d/my-cron

#CMD ["cron", "-f"]
CMD ["/usr/bin/supervisord"]
