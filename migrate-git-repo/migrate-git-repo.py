"""
Migrate a Git repository from one source to another.

Usage:
    migrate-git-repo.py <source> <destination> [--force]
"""
import json
import subprocess
import re

from loguru import logger as log
from pathlib import Path

####################################
# Update these variables
####################################
# SOURCE_REPO = "github.com/source.git"
# DESTINATION_REPO = "github.com/destination.git"
SOURCE_REPO = "https://github.com/cxmiller21/aws-sfn-sagemaker-demo.git"
DESTINATION_REPO = "https://github.com/cxmiller21/temp-test.git"
ENFORCE_GIT_LEAKS = True

# Global Variables (Do not update)
GIT_LEAKS_FILE_NAME = "gitleaks-report.json"


def is_valid_git_url(url: str) -> bool:
    """Check if the URL is a valid GitHub or GitLab Git URL"""
    github_pattern = r"^https?://github\.com/[\w-]+/[\w-]+(\.git)?$"
    gitlab_pattern = r"^https?://gitlab\.com/[\w-]+/[\w-]+(\.git)?$"
    return bool(re.match(github_pattern, url) or re.match(gitlab_pattern, url))


def verify_variables():
    """Verify that the variables are updated"""
    if not is_valid_git_url(SOURCE_REPO):
        raise ValueError("Invalid SOURCE_REPO Git URL")
    if not is_valid_git_url(DESTINATION_REPO):
        raise ValueError("Invalid DESTINATION_REPO Git URL")
    log.info("Variables are valid")


def get_repo_name_from_url(url: str) -> str:
    """Get the repository name from the Git URL"""
    return url.split("/")[-1].split(".")[0].replace(".git", "")


def create_dir(temp_dir_name: str) -> None:
    subprocess.run(["mkdir", "-p", temp_dir_name], check=True)


def clone_repo_to_temp_dir(repo_url: str, repo_name: str, temp_dir_name: str) -> str:
    """Clone a Git repository to a temporary directory"""
    log.info(f"Cloning {repo_url} to the temporary directory: '{temp_dir_name}'")
    subprocess.run(
        ["git", "clone", "--mirror", repo_url, f"{temp_dir_name}/{repo_name}"],
        check=True,
    )


def generate_git_leaks_findings(repo_name: str, temp_dir_name: str) -> None:
    """Scan a Git repository for Git leaks"""
    log.info(f"Scanning {temp_dir_name}/{repo_name} for Git leaks")
    subprocess.run(
        [
            "gitleaks",
            "detect",
            "--report-path",
            GIT_LEAKS_FILE_NAME,
            "-s",
            f"{temp_dir_name}/{repo_name}",
        ],
        check=True,
    )


def read_git_leaks_findings() -> bool:
    """Read the Gitleaks report file and return True if there are leaks"""
    with open(GIT_LEAKS_FILE_NAME) as f:
        data = json.load(f)
        if not data:
            return False
        if data["Leaks"]:
            return True


def migrate_repo_to_destination(repo_name: str, temp_dir_name: str) -> None:
    """Migrate a Git repository to the destination"""
    log.info(f"Migrating {temp_dir_name}/{repo_name} to {DESTINATION_REPO}")
    subprocess.run(
        [
            "git",
            "push",
            "--mirror",
            DESTINATION_REPO,
        ],
        cwd=f"{temp_dir_name}/{repo_name}",
        check=True,
    )


def main():
    """Main function"""
    verify_variables()

    # Clean up any existing files
    if Path(GIT_LEAKS_FILE_NAME).exists():
        # Delete the Git leaks file if it exists
        Path(GIT_LEAKS_FILE_NAME).unlink()
    if Path("./tmp").exists():
        # Delete the temporary directory if it exists
        Path("./tmp").rmdir()

    log.info(f"Source repo to clone: {SOURCE_REPO}")
    log.info(f"Destination repo to push to: {DESTINATION_REPO}")
    log.info(f"Enforce Git leaks: {ENFORCE_GIT_LEAKS}")

    temp_dir_name = "./tmp"
    create_dir(temp_dir_name)

    # Clone and scan the source repo for Git leaks
    repo_name = get_repo_name_from_url(SOURCE_REPO)
    clone_repo_to_temp_dir(SOURCE_REPO, repo_name, temp_dir_name)
    generate_git_leaks_findings(repo_name, temp_dir_name)

    has_leaks = read_git_leaks_findings()
    if not has_leaks:
        log.info("No Git leaks found. Safe to migrate repo")
    else:
        log.warning("Git leaks found!!!")
        if ENFORCE_GIT_LEAKS:
            raise ValueError("Git leaks found")

    # Migrate the repo to the destination
    migrate_repo_to_destination(repo_name, temp_dir_name)


if __name__ == "__main__":
    main()
