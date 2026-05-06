import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")


def get_repo_info(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()


def get_file_content(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r.text
