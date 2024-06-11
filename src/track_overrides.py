import os
import re
import requests
import sys
from typing import List, Dict
import textwrap


def parse_comments(file_path: str) -> List[Dict[str, str]]:
    pattern = r'HASH:\s*([a-f0-9]+)\s*REPO:\s*(https://github.com/\S+/)\s*PATH:\s*([\w/]+\.py)\s*METHOD:\s*(\w+)'
    with open(file_path, 'r') as file:
        content = file.read()
    matches = re.findall(pattern, content)
    overrides = [{'hash': match[0], 'repo': match[1], 'path': match[2], 'method': match[3]} for match in matches]
    return overrides


def get_latest_commit_hash(repo: str, path: str, method: str) -> str:
    try:
        if 'def' not in method:
            method = f'def {method}'
        api_url = f"https://api.github.com/repos/{repo.split('github.com/')[1]}commits"
        branch = os.getenv("GITHUB_BASE_REF")
        params = {'path': path, 'sha': branch}
        github_token = os.getenv("GITHUB_TOKEN")
        headers = {'Accept': 'application/vnd.github.v3+json',  'Authorization': f'token {github_token}'}
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        commits = response.json()
        for commit in commits:
            commit_sha = commit['sha']
            commit_details_url = f"https://api.github.com/repos/{repo.split('github.com/')[1]}commits/{commit_sha}"
            commit_details_response = requests.get(commit_details_url, headers=headers)
            commit_details_response.raise_for_status()
            commit_details = commit_details_response.json()
            for commit_file in commit_details['files']:
                if commit_file['filename'] != path:
                    continue
    
                if method in commit_file.get('patch', ''):
                    return commit_sha, commit_file.get('patch')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching latest commit hash for {path}:{method} - {e}")
        return None, None
    return None, None


def compare_hashes(overrides: List[Dict[str, str]]) -> List[str]:
    changed_methods = []
    for override in overrides:
        latest_commit_hash, patch = get_latest_commit_hash(override['repo'], override['path'], override['method'])
        if latest_commit_hash and latest_commit_hash != override['hash']:
            output = textwrap.dedent(f'''
            <details>

            <summary>`{override['method']}` in file `{override['path']}</summary>

            ```diff
            {patch}
            ```
            </details>
            '''.strip())
            changed_methods.append(output)
    return changed_methods

if __name__ == "__main__":
    app_directory = sys.argv[1]
    override_comments = []
    for root, _, files in os.walk(app_directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                override_comments.extend(parse_comments(file_path))
    
    changed_methods = compare_hashes(override_comments)
    pr_number = os.getenv("GITHUB_REF_NAME").split("/")[0]
    if changed_methods:
        if os.getenv("POST_COMMENT") in [True, 'true']:
            headers = {
                'Authorization': f'token {os.getenv("GITHUB_TOKEN")}',
                'Accept': 'application/vnd.github.v3+json'
            }
            override = {
                "method": "method",
                "path": "file"
            }
            url = f'https://api.github.com/repos/{os.getenv("GITHUB_REPOSITORY")}/issues/{pr_number}/comments'
            data = {'body': "\n".join(changed_methods)}
            response = requests.post(url, headers=headers, json=data)


        print("\n".join(changed_methods))

