#!/bin/sh
set -e

# Escape backslash and double-quote so API_BASE_URL can't break out of the JS string
# literal below (the value comes from a Container App env var we control, but this
# keeps the script safe even if that ever changes).
escaped_url=$(printf '%s' "${API_BASE_URL:-}" | sed 's/\\/\\\\/g; s/"/\\"/g')

cat <<EOF > /usr/share/nginx/html/config.js
window.__RUNTIME_CONFIG__ = { API_BASE_URL: "${escaped_url}" };
EOF
