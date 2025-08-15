#!/bin/bash
set -euo pipefail

echo "🔬 Running tests with 'task ci'..."
if ! task ci; then
    echo "❌ Tests failed. Aborting release."
    exit 1
fi

# Get version from argument or prompt
if [ -n "${1:-}" ]; then
  version="$1"
else
  read -rp "Enter release version (e.g., 1.2.3): " version
fi

if [ -z "$version" ]; then
  echo "❌ Version cannot be empty"
  exit 1
fi

# Check for uncommitted changes
stashed=0
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "💾 Detected uncommitted changes. Stashing..."
  git stash push -u -m "release-script-stash"
  stashed=1
  echo "✅ Changes stashed."
fi

# Update main branch
echo "🚀  Creating new release branch..."
git fetch origin main
git checkout -B main origin/main
git pull origin main
git checkout -b "release/v$version"

# Restore stashed changes if needed
if [ "$stashed" -eq 1 ]; then
  echo "♻️  Restoring stashed changes..."
  if git stash list | grep -q "release-script-stash"; then
    git stash pop || {
      echo "⚠️  Failed to apply stashed changes automatically. Please resolve conflicts manually."
    }
    echo "✅ Changes restored."
  else
    echo "⚠️  No matching stash found. Skipping restore."
  fi
fi

# Generate changelog
echo "📝  Generating changelog for version $version..."
python3 utils/generate_changelog.py "$version" || {
  echo "❌ Changelog generation failed."
  exit 1
}
if [ ! -f "changelog/v$version.md" ]; then
  echo "❌ changelog/v$version.md not found"
  exit 1
fi

echo "✅ Changelog generated:"
echo "---------------------------------------------"
cat "changelog/v$version.md"
echo "---------------------------------------------"
read -rp "Press Enter to continue with the release, or Ctrl+C to abort..."

# Update version in pyproject.toml
echo "🔄  Updating version in pyproject.toml to $version..."
sed -i.bak -E "s/^(version *= *\").*(\")/\1$version\2/" pyproject.toml
rm pyproject.toml.bak
uv sync
echo "✅  Version updated in pyproject.toml."

# Commit changes
echo "💾  Committing changelog and pyproject.toml..."
git add "changelog/v$version.md" pyproject.toml uv.lock
git commit -m "chore: bump version to v$version"
echo "✅  Commit created."

# Push release branch
echo "🔄  Pushing release branch..."
git push --set-upstream origin "release/v$version"
echo "✅  Branch pushed."

gh pr create --base main --head "release/v$version" \
  --title "Release v$version" \
  --body-file "changelog/v$version.md"

pr_url=$(gh pr view "release/v$version" --json url -q ".url")
echo "✅  Pull request created: $pr_url"

echo
echo "🛑 Merge the PR before continuing:"
echo "$pr_url"
echo
read -rp "Press Enter after the PR is merged, or Ctrl+C to abort..."

# Tag and release
echo "🔄  Updating local main branch..."
git checkout main
git pull origin main

if git rev-parse "v$version" >/dev/null 2>&1; then
  echo "❌ Tag v$version already exists"
  exit 1
fi

echo "🏷️  Creating git tag v$version..."
git tag -a "v$version" -m "Release v$version"

echo "🔄  Pushing tag..."
git push origin "v$version"

echo "🔄  Switching to main branch..."
git checkout main
git pull origin main

if git branch --merged main | grep -q "release/v$version"; then
    git branch -d "release/v$version"
else
    echo "⚠️  release/v$version not fully merged into main. Use -D to force delete."
fi

echo "🚀  Creating GitHub Release..."
gh release create "v$version" \
  --title "Release v$version" \
  --notes-file "changelog/v$version.md"

echo "✅  Release process completed for v$version."
