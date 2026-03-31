#!/bin/bash
source .env

echo "Enter MFA code:"
read -r MFA_CODE

OUTPUT=$(AWS_ACCESS_KEY_ID=$AWS_PERMANENT_ACCESS_KEY_ID \
         AWS_SECRET_ACCESS_KEY=$AWS_PERMANENT_SECRET_ACCESS_KEY \
         aws sts get-session-token \
           --serial-number "$AWS_MFA_SERIAL" \
           --token-code "$MFA_CODE" \
           --duration-seconds 43200)

aws configure set aws_access_key_id "$(echo "$OUTPUT" | python3 -c "import sys,json; print(json.load(sys.stdin)['Credentials']['AccessKeyId'])")"
aws configure set aws_secret_access_key "$(echo "$OUTPUT" | python3 -c "import sys,json; print(json.load(sys.stdin)['Credentials']['SecretAccessKey'])")"
aws configure set aws_session_token "$(echo "$OUTPUT" | python3 -c "import sys,json; print(json.load(sys.stdin)['Credentials']['SessionToken'])")"

echo "✅ AWS credentials refreshed!"