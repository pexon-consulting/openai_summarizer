locals {
  secret_env_vars = [for env_var in var.secret_env_vars : {
    name = env_var.name
    value_source = {
      secret_key_ref = {
        name = env_var.key_ref,
        key  = tostring(env_var.version)
      }
    }
  }]
}

resource "google_cloud_run_v2_job" "default" {
  name     = "${var.instance_name}-${var.environment}"
  location = var.location

  template {
    template {
      containers {
        image = "${var.location}-docker.pkg.dev/${var.project}/${var.container_registry_name}-${var.environment}/${var.image_name}:${var.image_tag}"

        dynamic "env" {
          for_each = var.env_vars
          content {
            name = env.value["name"]
            value = env.value["value"]
          }
        }

        dynamic "env" {
          for_each = var.secret_env_vars
          content {
            name = env.value["name"]
            value_source {
              secret_key_ref {
                secret = env.value["key_ref"]
                version = tostring(env.value["version"])
              }
            }
          }
        }
      }

      service_account = data.google_service_account.cloud_run_deployer.email
    }
  }

  lifecycle {
    ignore_changes = [
      launch_stage,
    ]
  }
}

