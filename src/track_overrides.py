import requests
import os
import re
import sys


def get_last_commit_hash_for_file_in_branch(repo_url, file_path):
    repo_url_split = repo_url.strip('/').split('/')
    username, repo_name = repo_url_split[-2], repo_url_split[-1]
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    branch = os.getenv("GITHUB_BASE_REF")
    params = {'path': file_path, 'sha': branch}
    response = requests.get(api_url, params=params)
    
    if response.status_code != 200:
        print(f"Failed to fetch commits: {response.status_code} - {response.reason}")
        return None

    commits = response.json()
    if commits:
        return commits[0]['sha']
    return None


def compare_commit_hashes(directory):
    changed_methods = []
    pattern = r"HASH:\s*(\w+)\s*REPO:\s*([\w\/:.]+)\s*PATH:\s*([\w\/.]+)\s*METHOD:\s*([\w]+)"

    for root, _, files in os.walk(directory):
        for file_name in files:
            if not file_name.endswith('.py'):
                continue
            
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                source_code = file.read()
                for match in re.finditer(pattern, source_code, re.DOTALL):
                    commit_hash = match.group(1)
                    repo = match.group(2)
                    file_path = match.group(3)
                    method_name = match.group(4)
                    latest_commit_hash = get_last_commit_hash_for_file_in_branch(repo, file_path)
                    if latest_commit_hash and latest_commit_hash != commit_hash:
                        changed_methods.append(f"Override method '{method_name}' in file '{file_path}' has changed in the upstream repository.")
    return changed_methods


if __name__ == "__main__":
    changed_methods = compare_commit_hashes(sys.argv[1])
    if changed_methods:
        print("\n".join(changed_methods)) 
