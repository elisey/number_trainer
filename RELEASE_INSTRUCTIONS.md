# Release Instructions for AI Agent

This document provides step-by-step instructions for releasing a new version of the number-trainer application.

## Prerequisites

- Ensure you have `gh` CLI tool installed and authenticated
- Ensure you have write access to the repository
- Make sure all tests pass before starting the release process

## Release Process

### Step 1: Version Bump

1. **Determine the new version number** based on the changes:
   - Patch (0.1.0 → 0.1.1): Bug fixes and minor improvements
   - Minor (0.1.0 → 0.2.0): New features, backward compatible
   - Major (0.1.0 → 1.0.0): Breaking changes

2. **Update the version in `pyproject.toml`**:
   ```bash
   # Edit the version field in [project] section
   version = "X.Y.Z"  # Replace with new version
   ```

### Step 2: Create Release Branch and Commit

1. **Create a new branch from fresh main/master**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b release/vX.Y.Z
   ```

2. **Commit the version bump**:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to vX.Y.Z"
   ```

### Step 3: Create Pull Request

1. **Push the release branch**:
   ```bash
   git push origin release/vX.Y.Z
   ```

2. **Create a Pull Request using gh CLI**:
   ```bash
   gh pr create \
     --title "Release vX.Y.Z" \
     --body "Release version X.Y.Z

   ## Changes
   - [List major changes here]

   ## Checklist
   - [ ] Version bumped in pyproject.toml
   - [ ] All tests passing
   - [ ] Documentation updated (if needed)
   - [ ] Ready for release" \
     --base main
   ```

### Step 4: Wait for PR Merge

**IMPORTANT**: Wait for the user to review and merge the PR. Do not proceed until the PR is merged.

### Step 5: Create and Push Tag

1. **Switch to fresh main branch**:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create an annotated tag**:
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   ```

3. **Ask for user confirmation before pushing**:
   ```
   I'm about to push the vX.Y.Z tag to the repository.
   Please confirm that:
   - The PR has been merged successfully
   - All changes look correct
   - You're ready for the release

   Type 'yes' to proceed with pushing the tag.
   ```

4. **Push the tag** (only after user confirmation):
   ```bash
   git push origin vX.Y.Z
   ```

### Step 6: Create GitHub Release (Optional)

If the repository uses GitHub releases, you can create one:

```bash
gh release create vX.Y.Z \
  --title "Release vX.Y.Z" \
  --notes "## What's Changed
  - [List major changes here]

  ## Installation
  \`\`\`bash
  pip install number-trainer==X.Y.Z
  \`\`\`"
```

## Example Commands for v0.2.0 Release

```bash
# Step 1: Update version in pyproject.toml to "0.2.0"

# Step 2: Create branch and commit
git checkout main
git pull origin main
git checkout -b release/v0.2.0
git add pyproject.toml
git commit -m "Bump version to v0.2.0"
git push origin release/v0.2.0

# Step 3: Create PR
gh pr create \
  --title "Release v0.2.0" \
  --body "Release version 0.2.0

## Changes
- [List changes here]

## Checklist
- [ ] Version bumped in pyproject.toml
- [ ] All tests passing
- [ ] Documentation updated (if needed)
- [ ] Ready for release" \
  --base main

# Step 4: Wait for PR merge...

# Step 5: Create and push tag
git checkout main
git pull origin main
git tag -a v0.2.0 -m "Release v0.2.0"
# Ask for confirmation
git push origin v0.2.0
```

## Important Notes

- **Always create release branches from fresh main/master**
- **Never skip the PR review process**
- **Always ask for user confirmation before pushing tags**
- **Use semantic versioning principles**
- **Include meaningful commit messages and PR descriptions**
- **Test the application before releasing**

## Troubleshooting

If something goes wrong during the release process:

1. **If PR needs changes**: Update the release branch and push again
2. **If tag was pushed incorrectly**: Delete the tag and recreate it
3. **If main branch is ahead**: Always pull latest changes before creating tags

## Version Numbering Guidelines

- **Patch (0.1.0 → 0.1.1)**: Bug fixes, documentation updates
- **Minor (0.1.0 → 0.2.0)**: New features, backward compatible changes
- **Major (0.1.0 → 1.0.0)**: Breaking changes, major refactoring

Follow semantic versioning (https://semver.org/) for consistent version numbering.
