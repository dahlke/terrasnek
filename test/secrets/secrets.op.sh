#!/bin/bash

eval $(op signin)

# Terraform Cloud/Enterprise Creds
export TFC_URL="https://app.terraform.io"

export TFC_TOKEN=$(op item get "Terraform Cloud" --format=json | jq -r '.fields[3].value')
export TFC_ORG_TOKEN=$(op item get "Terraform Cloud" --format=json | jq -r '.fields[4].value')

# SSL config
export SSL_VERIFY="true"

# AWS Credentials
export AWS_ACCESS_KEY_ID=$(op item get Amazon --format=json | jq -r '.fields[3].value')
export AWS_SECRET_ACCESS_KEY=$(op item get Amazon --format=json | jq -r '.fields[4].value')

# GitHub Secrets for VCS OAuth
export GH_TOKEN=$(op item get GitHub --format=json | jq -r '.fields[3].value')
export GH_SECRET=$(op item get GitHub --format=json | jq -r '.fields[4].value')

# Twilio Secrets for Admin Settings Testing
export TWILIO_ACCOUNT_SID=$(op item get Twilio --format=json | jq -r '.fields[3].value')
export TWILIO_AUTH_TOKEN=$(op item get Twilio --format=json | jq -r '.fields[4].value')

# SMTP Secrets for Admin Settings Testing
export SMTP_HOST=$(op item get Sendgrid --format=json | jq -r '.fields[3].value')
export SMTP_PORT=$(op item get Sendgrid --format=json | jq -r '.fields[4].value')
export SMTP_USERNAME=$(op item get Sendgrid --format=json | jq -r '.fields[5].value')
export SMTP_PASSWORD=$(op item get Sendgrid --format=json | jq -r '.fields[6].value')

# Constants used for creation and testing
export TEST_EMAIL="neil.dahlke+terrasnek_unittest@gmail.com"
# export TEST_ORG_NAME="terrasnek-unittest"
export TEST_ORG_NAME="terrasnek-unittest"
export TEST_USERNAME="terrasnek-unittest"
export TEST_TEAM_NAME="terrasnek-unittest"
export TEST_PASSWORD=""

# CodeCov Credentials
export CODECOV_TOKEN=$(op item get CodeCov --format=json | jq -r '.fields[3].value')
