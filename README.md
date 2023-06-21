# blogpost_zusammenfassung_automation

## Installation

Container einfach auf gewünschter plattform Deployen.
Dockerimage z.B mit folgendem Befehl bauen:

```bash
docker build -t automation_blogpost ../blogpost_zusammenfassung_automation/
```

## Usage

Es müssen einige Variablen gesetzt werden:

| Variable            | Value                                              |
| ------------------- | -------------------------------------------------- |
| base_url            | base URL of your confluence instance               |
| confluence_username | Confluence user with permission to read blog posts |
| confluence_token    | API token of your confluence service user          |
| openai_api_key      | OpenAI API key                                     |
| slack_token         | Slackbot API token                                 |
| slack_channel       | Slack channel ID                                   |



This bot checks what blog post it last summarized, then checks if there are any new blog post since it's last summary. If so, it takes the content of the blog post from the Confluence API, and uses the ChatGPT API to create a short summary of it, and posts it along with a link to the blog post into the configured slack channel. 





es werden unter /apps/logs zwei Logs erstellt. <br>
einmal das script.log .<br>
Dort ein Laufzeitlog aus dem Script geschrieben.<br>
Zweitens ein history.txt .<br>
Diese Datei wird benutzt um zu vergleichen ob der letzte Blogpost bereits zusammengefasst wurde und an Slack gesendet wurde.<br>
Darin werden die ID's der Confluenceseiten geschrieben, welche bereits zusammengefasst wurden. Damit soll Spam vermieden werden.<br>
Diese Dateien sollten bestmöglich in einem persistenten Volume gespeichert werden. Am wichtigsten ist jedoch die history.txt .<br>

## Support

Bei Fragen oder Verbesserungsvoschläge könnt ihr mich einfach anschreiben
