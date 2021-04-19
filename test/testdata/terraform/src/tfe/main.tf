variable "email" {
  type = string
}

variable "org_name" {
  type = string
}

variable "hostname" {
  type = string
  default = "app.terraform.io"
}

provider "tfe" {
  hostname = var.hostname
  ssl_skip_verify = true
}

resource "tfe_organization" "org" {
  email = "${var.email}"
  name = "${var.org_name}"
}

output "org_id" {
  value = "${tfe_organization.org.id}"
}