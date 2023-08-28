#!/bin/bash

# NOTE: these are all secrets. While some times it may be necessary to set these
# as secrets, I prefer having them all encrypted.

source ./scripts/shell/secrets.op.sh

gh secret set TFC_URL -b $TFC_URL
gh secret set TFC_TOKEN -b $TFC_TOKEN
gh secret set TFC_ORG_TOKEN -b $TFC_ORG_TOKEN
gh secret set SSL_VERIFY -b $SSL_VERIFY
gh secret set AWS_ACCESS_KEY_ID -b $AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY -b $AWS_SECRET_ACCESS_KEY
gh secret set GH_TOKEN -b $GH_TOKEN
gh secret set GH_SECRET -b $GH_SECRET
gh secret set TWILIO_ACCOUNT_SID -b $TWILIO_ACCOUNT_SID
gh secret set TWILIO_AUTH_TOKEN -b $TWILIO_AUTH_TOKEN
gh secret set SMTP_HOST -b $SMTP_HOST
gh secret set SMTP_PORT -b $SMTP_PORT
gh secret set SMTP_USERNAME -b $SMTP_USERNAME
gh secret set SMTP_PASSWORD -b $SMTP_PASSWORD
gh secret set TEST_EMAIL -b $TEST_EMAIL
gh secret set TEST_ORG_NAME -b $TEST_ORG_NAME
gh secret set TEST_ORG_NAME -b $TEST_ORG_NAME
gh secret set TEST_USERNAME -b $TEST_USERNAME
gh secret set TEST_TEAM_NAME -b $TEST_TEAM_NAME
gh secret set TEST_PASSWORD -b $TEST_PASSWORD
gh secret set CODECOV_TOKEN -b $CODECOV_TOKEN
