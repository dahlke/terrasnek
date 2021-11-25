#!/bin/bash

# Terraform Cloud/Enterprise Creds
export TFC_URL=""
export TFC_TOKEN=""

# SSL config
export SSL_VERIFY="true"

# AWS Credentials
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""

# GitHub Secrets for VCS OAuth
export GITHUB_TOKEN=""

# Twilio Secrets for Admin Settings Testing
export TWILIO_ACCOUNT_SID=""
export TWILIO_AUTH_TOKEN=""

# SMTP Secrets for Admin Settings Testing
export SMTP_HOST=""
export SMTP_PORT=""
export SMTP_USERNAME=""
export SMTP_PASSWORD=""

# Constants used for creation and testing
export TEST_EMAIL=""
export TEST_ORG_NAME=""
export TEST_USERNAME=""
export TEST_TEAM_NAME=""
export TEST_PASSWORD=""

# Variable used for uploading the above variables to CircleCI
# It is not used at all in the library
export CIRCLECI_TOKEN=""