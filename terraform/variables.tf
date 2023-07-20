variable "project" {
  type        = string
  description = "Google Project ID"
}

variable "environment" {
  type        = string
  description = "prod or dev"
}

variable "location" {
  type        = string
  description = "Cloud Run location"
  default     = "europe-west3"
}

variable "container_registry_name" {
  type        = string
  description = "Container registry name"
}

variable "min_instance_number" {
  type    = number
  default = 0
}

variable "max_instance_number" {
  type    = number
  default = 1
}

variable "image_name" {
  type        = string
  description = "Image name api used to deploy Cloud Run instance"
}

variable "image_tag" {
  type        = string
  description = "Image tag e.g. latest used to deploy Cloud Run instance"
}

variable "env_vars" {
  type = list(object({
    name  = string
    value = string
  }))
  default = []
}

variable "secret_env_vars" {
  type = list(object({
    name    = string
    key_ref = string
    version = number
  }))
  default = []
}

variable "instances" {
  type = map(object({
    env_vars = list(object({
      name  = string
      value = string
    }))
  }))
}

variable "cloud_run_service_account_email" {
  type        = string
  description = "Cloud Run service account email"
}