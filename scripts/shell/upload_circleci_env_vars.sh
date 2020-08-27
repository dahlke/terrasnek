# Upload everything from secrets.sh
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"TFC_URL\", \"value\": \"${TFC_URL}\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"TFC_TOKEN\", \"value\": \"$TFC_TOKEN\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"SSL_VERIFY\", \"value\": \"$SSL_VERIFY\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"AWS_ACCESS_KEY_ID\", \"value\": \"$AWS_ACCESS_KEY_ID\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"AWS_SECRET_ACCESS_KEY\", \"value\": \"$AWS_SECRET_ACCESS_KEY\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"GITHUB_TOKEN\", \"value\": \"$GITHUB_TOKEN\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"GITHUB_SECRET\", \"value\": \"$GITHUB_SECRET\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"TWILIO_ACCOUNT_SID\", \"value\": \"$TWILIO_ACCOUNT_SID\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"TWILIO_AUTH_TOKEN\", \"value\": \"$TWILIO_AUTH_TOKEN\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"SMTP_HOST\", \"value\": \"$SMTP_HOST\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"SMTP_PORT\", \"value\": \"$SMTP_PORT\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"SMTP_USERNAME\", \"value\": \"$SMTP_USERNAME\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"SMTP_PASSWORD\", \"value\": \"$SMTP_PASSWORD\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"TEST_EMAIL\", \"value\": \"$TEST_EMAIL\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"TEST_USERNAME\", \"value\": \"$TEST_USERNAME\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"TEST_TEAM_NAME\", \"value\": \"$TEST_TEAM_NAME\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"TEST_PASSWORD\", \"value\": \"$TEST_PASSWORD\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"TEST_ORG_NAME\", \"value\": \"$TEST_ORG_NAME\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN
curl -X POST --header "Content-Type: application/json" -d "{ \"name\": \"CODECOV_TOKEN\", \"value\": \"$CODECOV_TOKEN\" }" https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN

# List all the variables to confirm everything took
curl https://circleci.com/api/v1.1/project/gh/dahlke/terrasnek/envvar?circle-token=$CIRCLECI_TOKEN