# Confluence Blogpost Summarizer

This bot checks what blog post it last summarized by checking past Slack messages, then checks if there are any new blog post since it's last summary. If so, it takes the content of the blog post from the Confluence API, and uses the ChatGPT API to create a short summary of it, and posts it along with a link to the blog post into the configured slack channel.

To initialize the bot, you need to make an initial run with the `INITIAL_BLOGPOST_ID` variable set. This will triger a message with a summary of the blog post. Then on subsequent runs, it will look for the last message. The variable needs to be unset on subsequent runs.

## Build

```bash
docker build -t automation_blogpost .
```

## Configuration

| Variable            | Value                                                                                                                                                           |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BASE_URL            | base URL of your confluence instance                                                                                                                            |
| CONFLUENCE_USERNAME | Confluence user with permission to read blog posts                                                                                                              |
| CONFLUENCE_TOKEN    | API token of your confluence service user                                                                                                                       |
| OPENAI_API_KEY      | OpenAI API key                                                                                                                                                  |
| SLACK_TOKEN         | Slackbot API token                                                                                                                                              |
| SLACK_CHANNEL       | Slack channel ID                                                                                                                                                |
| DEBUG               | If set, the script summarizes the latest blog post                                                                                                              |
| OPENAI_STATEMENT               | if set, the default is overwritten. <br> The default is 'Du bist Pexon und erstellst eine lockere Zusammenfassung. Fasse folgenden Text in maximal 150 Wörtern und Bulletpoints zusammen. Überschriften sollen mit einfachen "*" am anfang und ende großgeschrieben sein. Fange an mit "TL;DR:'                                                                                                              |
| INITIAL_BLOGPOST_ID | If set, summarizes the specified Blog post. Used to initialize the bot since it relies on the latest sent summary to determine the newer blogposts to summarize |
