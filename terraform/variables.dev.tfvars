environment             = "dev"
project                 = "pexon-internal-services"
instance_name           = "openai"
container_registry_name = "openai"
image_name              = "api"
cloud_run_service_account_email = "cloud-run-deploymer@pexon-internal-services-dev.iam.gserviceaccount.com"

env_vars = [
  {
    name  = "BASE_URL",
    value = "https://pexon.atlassian.net/wiki"
  },
  {
    name  = "CONFLUENCE_USERNAME",
    value = "pexon-automation01@pexon-consulting.de"
  },
  {
    name  = "SLACK_CHANNEL",
    value = "C05B0BRV4DA"
  },
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
