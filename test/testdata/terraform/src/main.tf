provider "tfe" {
  hostname = "app.terraform.io"
}

variable "email" {
  type = "string"
}

variable "org_name" {
  type = "string"
}

resource "tfe_organization" "test" {
  email = "${var.email}"
  name = "${var.org_name}"
}

output "org_id" {
  value = "${tfe_organization.test.id}"
}