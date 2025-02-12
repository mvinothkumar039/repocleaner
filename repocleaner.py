import os
import datetime
from github import Github

# Load GitHub Token from Environment Variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("Error: Please set the GITHUB_TOKEN environment variable.")
    exit(1)

# Connect to GitHub API
g = Github(GITHUB_TOKEN)

# Read repository names from the file
repo_list_file = "masterRepoList.txt"
if not os.path.exists(repo_list_file):
    print(f"Error: File '{repo_list_file}' not found.")
    exit(1)

with open(repo_list_file, "r") as f:
    repos = [line.strip() for line in f if line.strip()]

# Define the time window
time_window = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=365)

# Initialize summary data
deleted_branches_summary = {}

for repo_name in repos:
    print(f"\nProcessing repository: {repo_name}")

    try:
        repo = g.get_repo(repo_name)
        branches = repo.get_branches()
        stale_branches = []

        # Identify stale branches
        for branch in branches:
            commit = repo.get_branch(branch.name).commit
            commit_date = commit.commit.author.date

            if commit_date < time_window:
                stale_branches.append((branch.name, commit_date))

        if not stale_branches:
            print(f"No stale branches found in '{repo_name}'. Skipping.")
            continue

        # Display stale branches
        print("\n Stale Branches Found:")
        for idx, (branch_name, date) in enumerate(stale_branches, 1):
            print(f"{idx}. {branch_name} - Last commit: {date}")

        # Ask user for confirmation
        to_delete = input("\nEnter branch numbers to delete (comma-separated) or 'all' to delete all: ")
        to_delete_indices = []

        if to_delete.lower() == "all":
            to_delete_indices = list(range(len(stale_branches)))
        else:
            to_delete_indices = [int(i) - 1 for i in to_delete.split(",") if i.strip().isdigit()]
            to_delete_indices = [i for i in to_delete_indices if 0 <= i < len(stale_branches)]

        # Delete selected branches
        deleted_branches = []
        for i in to_delete_indices:
            branch_name = stale_branches[i][0]
            try:
                ref = repo.get_git_ref(f"heads/{branch_name}")
                ref.delete()
                deleted_branches.append(branch_name)
                print(f"Deleted branch: {branch_name}")
            except Exception as e:
                print(f"Error deleting branch {branch_name}: {e}")

        # Save deleted branches info
        if deleted_branches:
            deleted_branches_summary[repo_name] = deleted_branches

        # If all branches are stale, recommend deleting repo
        if len(deleted_branches) == len(stale_branches):
            print(f"All branches in '{repo_name}' were stale. Consider deleting the repository.")

    except Exception as e:
        print(f"Error processing repository {repo_name}: {e}")

# Generate final report
summary_file = "repoCleaner_summary.txt"
with open(summary_file, "w") as f:
    f.write("repoCleaner Execution Summary\n")
    f.write("=" * 40 + "\n")
    for repo, branches in deleted_branches_summary.items():
        f.write(f"\nRepository: {repo}\n")
        f.write("Deleted Branches:\n")
        for branch in branches:
            f.write(f"- {branch}\n")
    if not deleted_branches_summary:
        f.write("\nNo stale branches were deleted in this run.\n")

print(f"\nExecution summary saved to '{summary_file}'.")
