#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Parse arguments
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "=== DRY RUN MODE ==="
fi

# Ensure we're in a git repo
git rev-parse --git-dir >/dev/null 2>&1 || { echo "Error: not a git repo."; exit 1; }

# Ensure uv exists
command -v uv >/dev/null 2>&1 || { echo "Error: 'uv' not found on PATH."; exit 1; }

# Ensure on main
current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$current_branch" != "main" ]]; then
  echo "Error: You must be on 'main' to release."
  exit 1
fi

# Ensure clean tree
if [[ -n "$(git status --porcelain=v1)" ]]; then
  echo "Error: Uncommitted changes detected. Commit or stash first."
  exit 1
fi

# Ensure up to date with origin
git fetch origin --tags --prune
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})
if [[ "$LOCAL" != "$REMOTE" ]]; then
  if [[ "$LOCAL" = "$BASE" ]]; then
    echo "Error: Your local branch is behind origin/main. Pull/rebase first."
    exit 1
  elif [[ "$REMOTE" = "$BASE" ]]; then
    echo "Info: Your branch is ahead of origin/main (ok)."
  else
    echo "Error: Local and remote have diverged. Resolve before releasing."
    exit 1
  fi
fi

# Get current version
if ! current_version="$(uv version --short 2>/dev/null)"; then
  current_version="none"
fi
echo "Current version: ${current_version}"

# Prompt for bump type early (fail fast)
printf "Select bump (major, minor, patch, stable, alpha, beta, rc, post, dev): "
read -r new_version
if [[ ! "$new_version" =~ ^(major|minor|patch|stable|alpha|beta|rc|post|dev)$ ]]; then
  echo "Error: Invalid type."
  exit 1
fi

if [[ "$DRY_RUN" == true ]]; then
  echo "[DRY RUN] Would bump version with: uv bump $new_version"
  echo "[DRY RUN] Exiting without making changes."
  exit 0
fi

# Bump version with error handling
if ! uv bump "$new_version"; then
  echo "Error: uv bump failed."
  exit 1
fi

# Get new version and preflight tag
if ! version="$(uv version --short 2>/dev/null)"; then
  echo "Error: could not read new version after bump."
  exit 1
fi
[[ -z "$version" ]] && { echo "Error: version is empty."; exit 1; }

tag="v$version"
if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
  echo "Error: tag $tag already exists."
  exit 1
fi

# Commit changes
git add -A
git commit -m "chore: release $version"

# Create tag (signed if possible, otherwise annotated)
if git config user.signingkey >/dev/null 2>&1; then
  if gpg --list-secret-keys "$(git config user.signingkey)" >/dev/null 2>&1; then
    if ! git tag -s "$tag" -m "$tag"; then
      echo "Warning: Signed tag failed; falling back to annotated."
      git tag -a "$tag" -m "$tag"
    fi
  else
    git tag -a "$tag" -m "$tag"
  fi
else
  git tag -a "$tag" -m "$tag"
fi

# Confirmation before push
echo ""
echo "Ready to push:"
echo "  - Commit: chore: release $version"
echo "  - Tag: $tag"
printf "Proceed with push? (y/N): "
read -r confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  echo "Aborted. To clean up local changes:"
  echo "  git reset --hard HEAD~1"
  echo "  git tag -d $tag"
  exit 1
fi

# Atomic push (commit + tag together)
if ! git push --atomic origin main "$tag"; then
  echo "Error: Failed to push. Rolling back local commit and tag..."
  git tag -d "$tag" || true
  git reset --hard HEAD~1
  echo "Rollback complete. Remote was not modified."
  exit 1
fi


echo ""
echo "✓ Released version $version successfully."
echo "  Commit: $(git rev-parse HEAD)"
echo "  Tag: $tag"
echo "  Log: $log_file"