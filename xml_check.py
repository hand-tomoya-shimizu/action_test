import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from github import Github

def add_reviewers():
    print("@ add_reviewers()")
    g = Github(os.getenv('GITHUB_TOKEN'))
    
    with open('reviewers_test.csv', 'r') as f:
        reader = csv.reader(f)
        reviewers = []
        for row in reader:
            targetName = row[1]
            targetNames.append(targetName)
            print(f"@ targetName: {targetName}")
            
            user = g.get_user(targetName)
            reviewers.append(user)
            
    repo = g.get_repo( os.getenv('GITHUB_REPOSITORY') )
    pr_number = int(os.getenv('PR_NUMBER'))
    pr = repo.get_pull(pr_number)
    
    pr.create_review_request(reviewers=reviewers)
    
    return targetNames


# プルリクエストのURL
pull_request_url = os.environ['GITHUB_API_URL'] + '/repos/' + os.environ['GITHUB_REPOSITORY'] + '/pulls/' + os.environ['PR_NUMBER']
#print(f"@ pull_request_url: {pull_request_url}")

# APIリクエストを送信して、変更内容を取得する
response = requests.get(pull_request_url)
#print(f"@ response1: {response}")

pull_request_data = response.json()

# 変更されたファイルの内容を取得して、XMLファイルが含まれているか確認する
diff_url = pull_request_data['diff_url']
#print(f"@ diff_url: {diff_url}")

diff_response = requests.get(diff_url)
#print(f"@ response2: {response}")

diff_text = diff_response.text
#print(f"@ diff_text: {diff_text}")

if '.xml' in diff_text:
    reviewerNames = add_reviewers()
    
    print("プルリクエストでXMLファイルが変更されました")
    
    slack_token = os.environ['SLACK_BOT_TOKEN']
    
    client = WebClient(token=slack_token)
    
    channelName = os.environ['SLACK_CHANNEL']
    print(f"@ channelName: {channelName}")
    
    htmlUrl = pull_request_data['html_url']
    print(f"@ htmlUrl: {htmlUrl}")
    
    
    message = ""
    
    for reviewerName in reviewerNames:
        message += reviewerName + "\n"
    
    message += "プルリクエストでXMLファイルの変更を検知しました。\nレビューをお願いします。\n"
    message += htmlUrl
    
    try:
        response = client.chat_postMessage(channel=channelName, text=message)
        print("Slackへの通知が完了しました")
    except SlackApiError as e:
        print("Slackへの通知が失敗しました：{}".format(e))
else:
    print("プルリクエストでXMLファイルは変更されていません")

exit(0)


