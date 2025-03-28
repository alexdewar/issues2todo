"""Configuration for tidier output."""

import os

REPO_NAME_MAP = {
    "FROG": "UNIRAS",
    "virtual_rainforest_snakemake_template": "virtual_ecosystem",
    "MUSE_2.0": "MUSE",
}
REPO_BLACKLIST = set(("Solidity-GUI", "clockify-tui", "healthgps"))


GH_COMMAND = (
    "gh search issues --assignee {user} --archived=false --state open -L 1000 "
    "--json number,title,repository"
)
EDITOR_COMMAND = os.getenv("EDITOR").split()  # type:ignore
