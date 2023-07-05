import requests
import os
from github import Github

rawtoken = "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"
repository = "lijc210/woo-app"

token = os.getenv('GITHUB_TOKEN', rawtoken)
g = Github(token)
headers = {'Authorization': 'Bearer ' + rawtoken,
          'Accept': 'application/octet-stream','X-GitHub-Api-Version':'2022-11-28'}
session = requests.Session()

url = "https://github.com/lijc210/woo-app/releases/download/v0.0.2/520-happy_0.0.2_x64_zh-CN.msi"
url = "https://api.github.com/repos/lijc210/woo-app/releases/assets/115505705"
# asset_one: arbitrary file for 
response = session.get(url, stream = True, headers=headers)
print(response.status_code)
print(response.text)