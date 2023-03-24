import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# プルリクエストのURL
pull_request_url = os.environ['GITHUB_API_URL'] + '/repos/' + os.environ['GITHUB_REPOSITORY'] + '/pulls/' + os.environ['PR_NUMBER']
print(f"@ pull_request_url: {pull_request_url}")

# APIリクエストを送信して、変更内容を取得する
response = requests.get(pull_request_url)
print(f"@ response1: {response}")

pull_request_data = response.json()

# 変更されたファイルの内容を取得して、XMLファイルが含まれているか確認する
diff_url = pull_request_data['diff_url']
print(f"@ diff_url: {diff_url}")

diff_response = requests.get(diff_url)
print(f"@ response2: {response}")

diff_text = diff_response.text
print(f"@ diff_text: {diff_text}")

if '.xml' in diff_text:
    print("プルリクエストでXMLファイルが変更されました")
    
    slack_token = os.environ['SLACK_BOT_TOKEN']
    
    client = WebClient(token=slack_token)
    
    channelName = os.environ['SLACK_CHANNEL']
    print(f"@ channelName: {channelName}")
    
    htmlUrl = pull_request_data['html_url']
    print(f"@ htmlUrl: {htmlUrl}")
    
    message = "プルリクエストでXMLファイルの変更を検知しました。\nレビューをお願いします。\n"
    message += htmlUrl
    
    try:
        response = client.chat_postMessage(channel=channelName, text=message)
        print("Slackへの通知が完了しました")
    except SlackApiError as e:
        print("Slackへの通知が失敗しました：{}".format(e))
else:
    print("プルリクエストでXMLファイルは変更されていません")

exit(0)
