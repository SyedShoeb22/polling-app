import requests
from django.conf import settings

def upload_to_github(path, content):
    url = f'https://api.github.com/repos/{settings.GITHUB_REPO_ACTIVITY}/contents/{path}'
    headers = {
        'Authorization': f'token {settings.GITHUB_TOKEN_ACTIVITY}',
        'Content-Type': 'application/json',
    }
    data = {
        'message': 'Add PDF file to activity directory',
        'content': content,
        'branch': 'main',
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def check_file_exists_on_github(path):
    url = f'https://api.github.com/repos/{settings.GITHUB_REPO_ACTIVITY}/contents/{path}'
    headers = {
        'Authorization': f'token {settings.GITHUB_TOKEN_ACTIVITY}',
    }
    response = requests.get(url, headers=headers)
    return response.status_code 