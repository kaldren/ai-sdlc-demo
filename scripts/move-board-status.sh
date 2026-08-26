#!/usr/bin/env bash
set -euo pipefail

# Moves a GitHub issue's card on the project board's Status field.
#
# Usage: scripts/move-board-status.sh <issue-number> <status-name>
#   status-name must match one of the Status field's options exactly
#   (e.g. "Backlog", "Ready", "In progress", "In review", "Done").
#
# Resolves the target repo from the git remote and requires `gh` to be
# authenticated with the `project` scope (gh auth refresh -s project,read:project).

usage() {
  echo "Usage: $0 <issue-number> <status-name>" >&2
  exit 1
}

[ $# -eq 2 ] || usage

issue_number="$1"
status_name="$2"

owner="${PROJECT_OWNER:-kaldren}"
project_number="${PROJECT_NUMBER:-3}"

remote_url="$(git config --get remote.origin.url)"
repo_owner="$(echo "$remote_url" | sed -E 's#.*[:/]([^/]+)/([^/.]+)(\.git)?$#\1#')"
repo_name="$(echo "$remote_url" | sed -E 's#.*[:/]([^/]+)/([^/.]+)(\.git)?$#\2#')"

project_id="$(gh project list --owner "$owner" --format json \
  -q ".projects[] | select(.number==${project_number}) | .id")"
if [ -z "$project_id" ]; then
  echo "Could not resolve project id for owner=$owner number=$project_number" >&2
  exit 1
fi

item_id="$(gh project item-list "$project_number" --owner "$owner" --format json -L 100 \
  -q ".items[] | select(.content.number==${issue_number} and .content.repository==\"${repo_owner}/${repo_name}\") | .id")"
if [ -z "$item_id" ]; then
  echo "Issue #${issue_number} is not on project ${owner}/${project_number} (repo: ${repo_owner}/${repo_name})" >&2
  exit 1
fi

field_id="$(gh project field-list "$project_number" --owner "$owner" --format json \
  -q '.fields[] | select(.name=="Status") | .id')"
option_id="$(gh project field-list "$project_number" --owner "$owner" --format json \
  -q ".fields[] | select(.name==\"Status\") | .options[] | select(.name==\"${status_name}\") | .id")"

if [ -z "$option_id" ]; then
  echo "Unknown status \"${status_name}\" — check the Status field's options in the project." >&2
  exit 1
fi

gh project item-edit --id "$item_id" --project-id "$project_id" --field-id "$field_id" \
  --single-select-option-id "$option_id" >/dev/null

echo "Moved issue #${issue_number} to \"${status_name}\""
