import os
import re
import requests
import sys
from typing import List, Dict


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
            output = f"""
            <details>

            <summary>`{override['method']}` in file `{override['path']}</summary>

            ```python
            {patch}
            ```
            </details>
            """
            output = f'''
            ensure_unique_roles in file frappe/core/doctype/user/user.py 
            ```diff
                            @@ -481,10 +481,9 @@ def after_rename(self, old_name, new_name, merge=False):
                                has_fields.append(d.get("name"))
                        for field in has_fields:
                            frappe.db.sql(
            -					"""UPDATE `%s`
            -					SET `%s` = %s
            -					WHERE `%s` = %s"""
            -					% (tab, field, "%s", field, "%s"),
            +					"""UPDATE `{}`
            +					SET `{}` = {}
            +					WHERE `{}` = {}""".format(tab, field, "%s", field, "%s"),
                                (new_name, old_name),
                            )
            
            @@ -527,7 +526,7 @@ def remove_disabled_roles(self):
            
                def ensure_unique_roles(self):
                    exists = []
            -		for i, d in enumerate(self.get("roles")):
            +		for _i, d in enumerate(self.get("roles")):
                        if (not d.role) or (d.role in exists):
                            self.get("roles").remove(d)
                        else:
            @@ -991,7 +990,7 @@ def get_total_users():
            def get_system_users(exclude_users=None, limit=None):
                if not exclude_users:
                    exclude_users = []
            -	elif not isinstance(exclude_users, (list, tuple)):
            +	elif not isinstance(exclude_users, list | tuple):
                    exclude_users = [exclude_users]
            
                limit_cond = ""
            @@ -1081,7 +1080,7 @@ def handle_password_test_fail(feedback: dict):
                suggestions = feedback.get("suggestions", [])
                warning = feedback.get("warning", "")
            
            +	frappe.throw(msg=" ".join([warning, *suggestions]), title=_("Invalid Password"))
            
            
            def update_gravatar(name):
            ```
            '''
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
    if changed_methods:
        print("\n".join(changed_methods))

