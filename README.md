### Overview ###

repoCleaner is a Python-based GitHub utility that helps clean up stale repositories and branches. It reads a list of repositories from masterRepoList.txt, identifies branches older than a user-defined time window (default: 1 year), and provides an interactive option to delete stale branches.

### Features ###

* Reads repository list from masterRepoList.txt.
* Fetches all branches and their latest commit timestamps.
* Identifies stale branches older than 1 year (default threshold).
* Allows user selection to delete all, some, or none of the stale branches.
* Generates an execution summary detailing deleted branches.
* If all branches in a repo are stale, suggests repository deletion.
* Handles network failures with execution recovery.

### Setup Instructions ###

1. Create a GitHub Account

* If you don’t already have a GitHub account, create one at GitHub.

2. Generate a GitHub Personal Access Token (PAT)

* Go to GitHub Settings → Developer settings → Personal access tokens.
* Click Generate new token (classic).
* Select the required permissions:
* repo (Full control of private repositories)
* delete_repo (Only if you want to automate repository deletion)
* Copy and store the token securely (it won't be shown again).

3. Install Python and Set Up a Virtual Environment

$ sudo apt update && sudo apt install python3 python3-venv python3-pip -y $
$ mkdir repoCleaner && cd repoCleaner $
$ python3 -m venv venv $
$ source venv/bin/activate $

4. Install Dependencies

$ pip install PyGithub $

### Usage ###

1. Configure Repository List

Edit masterRepoList.txt to include repositories in owner/repo format:

$ nano masterRepoList.txt $

Example:
mvinothkumar039/docs
mvinothkumar039/gh-ost
mvinothkumar039/dmca
mvinothkumar039/DPG-guidance

2. Set Up GitHub Authentication

Create a .env file to store the GitHub token securely:

$ echo "GITHUB_TOKEN=your_personal_access_token" > .env $

3. Run the Script

$ python3 repocleaner.py $

4. Follow On-Screen Prompts

* The script will display stale branches and prompt for deletion.
* Select all, some, or none of the branches for deletion.
* An execution summary will be saved to repoCleaner_summary.txt.

* Example Execution:

Processing repository: mvinothkumar039/docs
Total branches: 5
Stale branches (>1 year): 2
  - branch1 (Last commit: 2022-01-15)
  - branch2 (Last commit: 2021-08-30)
Do you want to delete these branches? (yes/no/selective):
> selective
Enter branches to delete (comma-separated): branch1
  Deleted branch: branch1
  Summary saved to repoCleaner_summary.txt

### Troubleshooting ###

1. Error: 404 Not Found on Repositories
Ensure masterRepoList.txt contains repositories in owner/repo format (not full URLs).

2. Error: Authentication failed
Verify that the GitHub token is correctly stored in .env.

3. Virtual Environment Not Found
Activate it before running the script:

$ source venv/bin/activate $

4. How to Exit Virtual Environment?

$ deactivate $
