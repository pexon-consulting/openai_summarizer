# blogpost_zusammenfassung_automation


## Installation
Container einfach auf gewünschter plattform Deployen.
Dockerimage z.B mit folgendem Befehl bauen:

```bash
docker build -t automation_blogpost ../blogpost_zusammenfassung_automation/
```


## Usage
Es müssen einige Variablen gesetzt werden:
```
	- base_url					# https://pexon.atlassian.net/wiki
	- confluence_username		# Confluence user der berechtigung zum lesen der Blogposts hat
	- confluence_token			# API Token zum Confluence Service User
	- openai_api_key			# OpenAI API Token
	- slack_token				# Slackbot API Token
	- slack_channel 			# zum Beispiel der Internal-Service-Test Channel (C05B0BRV4DA)
	- CRON_SCHEDULE 			# standardmäßig wird '0 9-17 * * *' verwendet
```

es werden unter /apps/logs zwei Logs erstellt.
einmal das script.log .
Dort ein Laufzeitlog aus dem Script geschrieben.
Zweitens ein history.txt .
Diese Datei wird benutzt um zu vergleichen ob der letzte Blogpost bereits zusammengefasst wurde und an Slack gesendet wurde.
Darin werden die ID's der Confluenceseiten geschrieben, welche bereits zusammengefasst wurden. Damit soll Spam vermieden werden.
Diese Dateien sollten bestmöglich in einem persistenten Volume gespeichert werden. Am wichtigsten ist jedoch die history.txt .


## Support
Bei Fragen oder Verbesserungsvoschläge könnt ihr mich einfach anschreiben

