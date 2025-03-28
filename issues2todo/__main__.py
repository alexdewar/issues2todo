"""The entry point for the GitHub issue importer program."""

import json
import re
import subprocess as sp
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .config import EDITOR_COMMAND, GH_COMMAND, REPO_BLACKLIST, REPO_NAME_MAP


def main() -> None:
    """Main entrypoint."""
    run_script(sys.argv[1], Path(sys.argv[2]) if len(sys.argv) > 2 else None)


def run_script(user: str, todotxt_path: Path | None = None) -> None:
    """Run the script."""
    if not todotxt_path:
        todotxt_path = Path.home() / "todo.txt"

    ret = sp.run(GH_COMMAND.format(user=user).split(" "), capture_output=True)
    ret.check_returncode()
    issues: list[dict[str, Any]] = json.loads(ret.stdout)

    # Load existing todo items
    with todotxt_path.open() as file:
        todo_items = set(line.strip() for line in file.readlines())

    # Load issues from GitHub
    issue_items: list[str] = []
    for issue in issues:
        project = issue["repository"]["name"]
        if project in REPO_BLACKLIST:
            continue
        if mapped_name := REPO_NAME_MAP.get(project, None):
            project = mapped_name

        item = f"{issue['title']} (#{issue['number']}) +{project}"
        if item in todo_items:
            continue

        issue_items.append(item)

    # Sort by project for readability
    issue_items.sort(key=get_tag)

    # Write issues to file
    with NamedTemporaryFile("w", delete=False) as file:
        issues_path = file.name
        file.writelines(f"{issue}\n" for issue in issue_items)

    # Edit/select issues
    sp.run([*EDITOR_COMMAND, issues_path], check=True)

    # Reload issues
    with open(issues_path) as file:
        issue_items = file.readlines()

    # Append to todo list
    print(f"Adding {len(issue_items)} to todo list")
    with todotxt_path.open("a") as file:
        file.writelines(issue_items)


def get_tag(s: str) -> str:
    """Get the project tag."""
    if match := re.search(r"\+([^\+]+)$", s):
        return match.group(1)
    return ""


if __name__ == "__main__":
    main()
