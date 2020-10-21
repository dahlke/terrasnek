#!/bin/bash

eval $(op signin my)

# Terraform Cloud/Enterprise Creds
export TFC_URL="https://app.terraform.io"
export TFC_TOKEN=$(op get item "Terraform Cloud" | jq -r '.details.sections[1].fields[0].v')
export TFC_ORG_TOKEN=$(op get item "Terraform Cloud" | jq -r '.details.sections[1].fields[1].v')

# SSL config
export SSL_VERIFY="true"

# AWS Credentials
export AWS_ACCESS_KEY_ID=$(op get item Amazon | jq -r '.details.sections[1].fields[0].v')
export AWS_SECRET_ACCESS_KEY=$(op get item Amazon | jq -r '.details.sections[1].fields[1].v')

# GitHub Secrets for VCS OAuth
export GITHUB_TOKEN=$(op get item GitHub | jq -r '.details.sections[1].fields[0].v')
export GITHUB_SECRET=$(op get item GitHub | jq -r '.details.sections[1].fields[1].v')

# Twilio Secrets for Admin Settings Testing
export TWILIO_ACCOUNT_SID=$(op get item Twilio | jq -r '.details.sections[1].fields[0].v')
export TWILIO_AUTH_TOKEN=$(op get item Twilio | jq -r '.details.sections[1].fields[1].v')

# SMTP Secrets for Admin Settings Testing
export SMTP_HOST=$(op get item Sendgrid | jq -r '.details.sections[1].fields[0].v')
export SMTP_PORT=$(op get item Sendgrid | jq -r '.details.sections[1].fields[1].v')
export SMTP_USERNAME=$(op get item Sendgrid | jq -r '.details.sections[1].fields[2].v')
export SMTP_PASSWORD=$(op get item Sendgrid | jq -r '.details.sections[1].fields[3].v')

# Constants used for creation and testing
export TEST_EMAIL="neil.dahlke+terrasnek_unittest@gmail.com"
# export TEST_ORG_NAME="terrasnek-unittest"
export TEST_ORG_NAME="terrasnek-unittest"
export TEST_USERNAME="terrasnek-unittest"
export TEST_TEAM_NAME="terrasnek-unittest"
export TEST_PASSWORD=""

# CodeCov Credentials
export CODECOV_TOKEN=$(op get item CodeCov | jq -r '.details.sections[1].fields[0].v')

# Variable used for uploading the above variables to CircleCI
export CIRCLECI_TOKEN=$(op get item CircleCI | jq -r '.details.sections[1].fields[0].v')