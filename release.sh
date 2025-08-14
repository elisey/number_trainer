#!/bin/bash
set -euo pipefail

# Ensure working tree is clean
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "❌ Error: You have uncommitted changes. Please commit or stash them before running the release script."
  exit 1
fi

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

# Update main branch
echo "🚀  Creating new release branch..."
git fetch origin main
git checkout -B main origin/main
git pull origin main
git checkout -b "release/v$version"

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
echo "✅  Version updated in pyproject.toml."

# Commit changes
echo "💾  Committing changelog and pyproject.toml..."
git add "changelog/v$version.md" pyproject.toml
git commit -m "chore: bump version to v$version"
echo "✅  Commit created."

# Push release branch
echo "🔄  Pushing release branch..."
git push --set-upstream origin "release/v$version"
echo "✅  Branch pushed."

# Create a temporary body file
body_file=$(mktemp)
trap 'rm -f "$body_file"' EXIT
{
  echo "Release v$version"
  echo
  cat "changelog/v$version.md"
} > "$body_file"

gh pr create --base main --head "release/v$version" \
  --title "Release v$version" \
  --body-file "$body_file"

rm "$body_file"
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

echo "🚀  Creating GitHub Release..."
gh release create "v$version" \
  --title "Release v$version" \
  --notes-file "changelog/v$version.md"

echo "✅  Release process completed for v$version."
