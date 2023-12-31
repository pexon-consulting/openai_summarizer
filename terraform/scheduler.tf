resource "google_cloud_scheduler_job" "job" {
  for_each = var.instances
  name             = "openai-${each.key}-${var.environment}-scheduler-trigger"
  description      = "Trigger Cloud Run job to execute OpenAI Blog Post Bot"
  schedule         = each.value.schedule
  region = var.location
  time_zone        = "CET"
  attempt_deadline = "320s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = "https://${var.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project}/jobs/${each.key}-${var.environment}:run"
    headers = {
      "User-Agent" : "Google-Cloud-Scheduler"
    }

    oauth_token {
      service_account_email = data.google_service_account.cloud_run_deployer.email
    }
  }
}
