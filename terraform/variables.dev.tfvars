environment             = "dev"
project                 = "pexon-internal-services-dev"
instance_name           = "openai"
container_registry_name = "openai"
image_name              = "api"
cloud_run_service_account_email = "cloud-run-deploymer@pexon-internal-services-dev.iam.gserviceaccount.com"

instances = {
  "confluence" = {
    env_vars = [ 
      {
        name  = "MODE",
        value = "CONFLUENCE"
      },
      {
        name  = "SLACK_CHANNEL",
        value = "C02G0S79MPV"
      },
    ],
    schedule = "30 * * * *"
  },
  "azure" = {
    env_vars = [ 
      {
        name  = "MODE",
        value = "AZURE"
      },
      {
        name  = "SLACK_CHANNEL",
        value = "C02HQ87948N"
      },
    ],
    schedule = "0 21 * * *"
  }
}

env_vars = [
  {
    name  = "BASE_URL",
    value = "https://pexon.atlassian.net/wiki"
  },
  {
    name  = "CONFLUENCE_USERNAME",
    value = "pexon-automation01@pexon-consulting.de"
  }
]

secret_env_vars = [
  {
    name    = "OPENAI_API_KEY"
    key_ref = "OPENAI_API_KEY"
    version = 1
  },
  {
    name    = "CONFLUENCE_TOKEN"
    key_ref = "OPENAI_CONFLUENCE_TOKEN"
    version = 1
  },
  {
    name    = "SLACK_TOKEN"
    key_ref = "SANDBOX_SLACK_TOKEN"
    version = 1
  }
]
