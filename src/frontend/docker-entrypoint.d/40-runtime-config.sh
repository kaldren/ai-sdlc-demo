#!/bin/sh
set -e

cat <<EOF > /usr/share/nginx/html/config.js
window.__RUNTIME_CONFIG__ = { API_BASE_URL: "${API_BASE_URL:-}" };
EOF
