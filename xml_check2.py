import os
import subprocess
import requests
import json

# Slack の Webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXXXXXXXX/YYYYYYYYY/ZZZZZZZZZZZZZZZZZZZZZZZZ"

# プルリクエストに含まれる XML ファイルのパスを検索する正規表現
XML_FILE_PATTERN = "\.xml$"

# プルリクエストの差分に XML ファイルが含まれているかどうかを確認する関数
def is_xml_file_updated():
    diff_command = "git diff --name-only HEAD^..HEAD"
    diff_output = subprocess.check_output(diff_command, shell=True).decode()
    return any(path.endswith(".xml") for path in diff_output.split("\n"))

# Slack に通知する関数
def notify_slack():
    pr_url = os.environ.get("PULL_REQUEST_URL")
    message = f"XML file(s) updated in PR: {pr_url}"
    payload = {
        "text": message,
        "username": "GitHub Actions",
        "icon_emoji": ":robot_face:",
    }
    headers = {"Content-Type": "application/json"}
    
    print(f"@ payload: {payload}")
    
    #response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    #if response.status_code != 200:
    #    raise ValueError("Failed to send Slack notification")

if __name__ == "__main__":
    if is_xml_file_updated():
        notify_slack()
