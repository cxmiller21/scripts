# Migrate a Git repository from a source to a new destination

## Pre-requisites

- [Git](https://git-scm.com/)
- [GitLeaks](https://github.com/gitleaks/gitleaks)
- [GitHub CLI](https://cli.github.com/) (Optional)
- Source repository
  - Exists
  - CLI authentication to source repository is valid
- Destination repository
  - Exists and is empty
  - CLI authentication to destination repository is valid

## Automated Steps

1. Modify the variables in `migrate-git-repo.sh` to match your source and destination repositories
    ```bash
    SOURCE_REPO = ""
    DESTINATION_REPO = ""
    ENFORCE_GIT_LEAKS = True
    ```
2. Run the script
    ```bash
    ./migrate-git-repo.sh
    ```
3. Verify repository has been successfully migrated

## Manual Steps

1. Clone the source repository
    ```bash
    # Clone repo with all branches, tags, and history
    git clone --mirror url-to-source-repo.git

    # Clone repo with only the default branch
    git clone url-to-source-repo.git
    ```
2. Change into the cloned repository
    ```bash
    cd url-to-source-repo.git
    ```
3 .
