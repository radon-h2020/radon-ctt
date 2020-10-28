#!/usr/bin/env bash
echo -e "-----BEGIN ${KEY_TYPE} PRIVATE KEY-----\n$(echo ${SSH_PRIV_KEY} | sed 's/ /\n/g')\n-----END ${KEY_TYPE} PRIVATE KEY-----" > "${OPERA_SSH_IDENTITY_FILE}"
export SSH_PRIV_KEY=""
chmod 0600 "${OPERA_SSH_IDENTITY_FILE}"
python3 -m openapi_server