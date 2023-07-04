environment             = "prod"
project                 = "pexon-internal-services-dev"
instance_name           = "openai"
container_registry_name = "openai"
image_name              = "api"
cloud_run_service_account_email = "cloud-run-deploymer@pexon-internal-services.iam.gserviceaccount.com"

env_vars = [
  {
    name  = "DATABASE_HOST",
    value = "/cloudsql/pexon-internal-services-dev:europe-west3:sandboxes-dev"
  },
  {
    name  = "NODE_ENV"
    value = "development"
  },
  {
    name  = "COLORIZE_OUTPUT"
    value = "false"
  },
  {
    name = "APP_SLACK_BENCH_CHANNEL_MAX_DAYS_OLDEST_MESSAGE",
    value = 14
  },
  {
    name = "APP_DAYS_OFFSET",
    value = 4
  },
  {
    name = "APP_SLACK_BENCH_CHANNEL_MESSAGE_IDENTIFIER",
    value = "cttraining"
  },
  {
    name = "APP_SLACK_BENCH_CHANNEL_EMOJIS_CONFIRMED",
    value = "white_check_mark"
  },
  {
    name  = "COLORIZE_OUTPUT"
    value = "false"
  },
  {
    name  = "APP_SESSION_TYPES"
    value = "training,rhetorik"
  },
  {
    name  = "APP_SLACK_BENCH_CHANNEL_ID"
    value = "C01JS7Q5D41"
  },
  {
    name  = "APP_MEETING_NAME"
    value = "Consulting Training"
  },
  {
    name = "APP_SLACK_BENCH_CHANNEL_EMOJIS_TRAINER",
    value = "robot_face"
  },
]

secret_env_vars = [
  {
    name    = "APP_API_KEY"
    key_ref = "MALASTARE_API_KEY"
    version = 1
  },
  {
    name    = "APP_SLACK_TOKEN"
    key_ref = "SANDBOX_SLACK_TOKEN"
    version = 1
  },
  {
    name    = "APP_SLACK_SINGING_SECRET"
    key_ref = "SANDBOX_SLACK_SIGNING_SECRET"
    version = 1
  },
  {
    name    = "CALENDAR_SERVICE_ACCOUNT"
    key_ref = "MOCK_INTERVIEW_SERVICE_ACCOUNT"
    version = 1
  }
]
