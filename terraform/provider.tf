terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.72.0"
    }
  }
}

provider "google" {
  project = var.project
  region = var.location
}

data "google_service_account" "cloud_run_deployer" {
  account_id = var.cloud_run_service_account_email
}