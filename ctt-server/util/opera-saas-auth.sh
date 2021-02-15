#!/usr/bin/env bash

your_username="$1"
your_password="$2"
api="$3"
auth_base_url="$4"
# cookie_jar_path="$(mktemp)"
cookie_jar_path="/tmp/cookiejar_ctt.txt"
secret_base64="$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 - | head -n 1 | base64 -)"

shopt -s expand_aliases
alias cookiecurl="curl -sSL --cookie-jar $cookie_jar_path --cookie $cookie_jar_path"

response_from_credentials_redirected_to_next_auth="$(cookiecurl $api/secret)"
redirect_url_to_radonauth="$(echo $response_from_credentials_redirected_to_next_auth | xmllint --html --xpath "string(//a[@id='zocial-keycloak-xlab-oidc-provider-to-keycloak-radon']/@href)" - 2>/dev/null)"
response_radonauth="$(cookiecurl ${auth_base_url}${redirect_url_to_radonauth})"
login_url_radonauth="$(echo $response_radonauth | xmllint --html --xpath "string(//form[@id='kc-form-login']/@action)" - 2>/dev/null)"
cookiecurl "$login_url_radonauth" -d "username=$your_username" -d "password=$your_password" -d credentialId="" >/dev/null
redirect_url="$login_url_radonauth"
cookiecurl "$redirect_url" -d "username=$your_username" -d "password=$your_password" -d credentialId="" >/dev/null
echo "$cookie_jar_path"
