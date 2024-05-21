# Track Overrides

`track-overrides` is a GitHub Action designed to track method overrides in Python projects. It compares the current state of the code against a base branch to identify any changes in overridden methods, which is particularly useful for maintaining custom modifications in large projects.

## Features

- **Automated Override Tracking**: Automatically track changes in overridden methods in your Python codebase on every Pull Request.
- **Dynamic Base Branch Detection**: Automatically detects the base branch from the pull request to compare against.

## Method Annotation

To track the overrides, the methods must have a comment with the following structure:

```
"""
HASH: <commit_hash>
REPO: <repository_url>
PATH: <file_path>
METHOD: <method_name>
"""
```

### Example
```python
def is_system_manager_disabled(user):
    """
    HASH: 171e1d0159cda3b8d9415527590c9c3ca0c827be
    REPO: https://github.com/frappe/frappe/
    PATH: frappe/core/doctype/user/user.py
    METHOD: is_system_manager_disabled
    """
    # Method implementation here
    pass
```

## Usage

To use the `track-overrides` GitHub Action in your workflow, follow these steps:

### 1. Create a Workflow File

Create a new GitHub Actions workflow file in your repository, e.g., `.github/workflows/overrides.yml`, and add the following content:

```yaml
name: Track Overrides

on:
  pull_request:

jobs:
  track_overrides:
    runs-on: ubuntu-latest
    name: Track Overrides
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name:  Track Overrides
        uses: diamorafaela/track-overrides@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```