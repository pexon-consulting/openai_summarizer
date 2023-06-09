#!/bin/sh

echo "$CRON_SCHEDULE root python /app/automation.py >> /var/log/cron.log 2>&1" > /etc/cron.d/mycron

chmod 0644 /etc/cron.d/mycron

cron #&& tail -f /var/log/cron.log