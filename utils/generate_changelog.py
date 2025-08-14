#!/usr/bin/env python3
import sys
import subprocess
from datetime import datetime
import re
from pathlib import Path

def run(cmd, capture_output=True, text=True):
    """Run shell command and return output."""
    result = subprocess.run(cmd, capture_output=capture_output, text=text, check=True)
    return result.stdout.strip()

def get_latest_tag():
    try:
        return run(["git", "describe", "--tags", "--abbrev=0"])
    except subprocess.CalledProcessError:
        print("❌ No Git tags found. Cannot generate changelog.")
        sys.exit(1)

def get_github_repo():
    url = run(["git", "remote", "get-url", "origin"])
    ssh_match = re.match(r"git@github\.com:(.+)/(.+)\.git", url)
    https_match = re.match(r"https://github\.com/(.+)/(.+)\.git", url)
    if ssh_match:
        return ssh_match.group(1), ssh_match.group(2)
    elif https_match:
        return https_match.group(1), https_match.group(2)
    else:
        print("❌ Could not parse GitHub repository from remote URL.")
        sys.exit(1)

def get_merge_commits(start_tag):
    log_format = "%H%n%ad%n%s%n%b%n--END--"
    output = run([
        "git", "log", f"{start_tag}..HEAD", "--merges",
        f"--pretty=format:{log_format}", "--date=short"
    ])
    commits = []
    for block in output.split("--END--"):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n")
        commit_hash, date, title = lines[:3]
        body = lines[3:]
        pr_link = ""
        pr_match = re.match(r"Merge pull request #(\d+)", title)
        if pr_match:
            pr_number = pr_match.group(1)
            user, repo = get_github_repo()
            pr_link = f"https://github.com/{user}/{repo}/pull/{pr_number}"
            title_with_link = f"[{title}]({pr_link})"
        else:
            title_with_link = title
        commits.append({
            "date": date,
            "title": title_with_link,
            "body": body
        })
    return commits

def generate_changelog_section(version, commits):
    today = datetime.today().strftime("%Y-%m-%d")
    lines = [f"## {version}", f"### {today}", ""]
    for commit in commits:
        lines.append(f"- {commit['title']} ({commit['date']})")
        for body_line in commit["body"]:
            if body_line.strip():
                lines.append(f"  {body_line}")
        lines.append("")
    return "\n".join(lines)

def write_changelog_file(version, section):
    changelog_dir = Path("changelog")
    changelog_dir.mkdir(exist_ok=True)
    changelog_file = changelog_dir / f"{version}.md"
    changelog_file.write_text(section)
    print(f"✅ Changelog for version {version} written to {changelog_file}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} NEW_VERSION")
        sys.exit(1)

    new_version = sys.argv[1]
    start_tag = get_latest_tag()

    commits = get_merge_commits(start_tag)
    if not commits:
        print(f"ℹ️ No merge commits since {start_tag}. Changelog not created.")
        sys.exit(0)

    section = generate_changelog_section(new_version, commits)
    write_changelog_file(new_version, section)

if __name__ == "__main__":
    main()
