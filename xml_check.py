import os
import requests
import csv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from github import Github, UnknownObjectException

def add_reviewers():
    print("@ add_reviewers()")
    g = Github(os.getenv('GITHUB_TOKEN'))
    
    targetNames = []
    targetIds = []
    reviewers = []
    
    with open('reviewers.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            targetName = row[1]
            targetId = row[2]
            print(f"@ targetName: {targetName} ({targetId})")
            
            try:
                user = g.get_user(targetName)
                print(f"@ -> append.")
                
                reviewers.append(user)
                targetNames.append(targetName)
                targetIds.append(targetId)
                
            except UnknownObjectException:
                print(f"@ -> not exist.")
    
    if len(reviewers) > 0:
        repo = g.get_repo( os.getenv('GITHUB_REPOSITORY') )
        pr_number = int(os.getenv('PR_NUMBER'))
        pr = repo.get_pull(pr_number)
        author = pr.user
        
        for reviewer in reviewers:
            print(f"@ reviewer: {reviewer}")
            
            if reviewer == author:
                print("@ -> skipped.")
                continue
            
            try:
                print(f"@ reviewer.login: {reviewer.login}")
                pr.create_review_request(reviewers=[reviewer.login])
            except UnknownObjectException:
                print(f"@ Error: {reviewer.login} is not exist.")
                continue
    
    return targetIds


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
    reviewerIds = add_reviewers()
    
    print("プルリクエストでXMLファイルが変更されました")
    
    slack_token = os.environ['SLACK_BOT_TOKEN']
    
    client = WebClient(token=slack_token)
    
    channelName = os.environ['SLACK_CHANNEL']
    print(f"@ channelName: {channelName}")
    
    htmlUrl = pull_request_data['html_url']
    print(f"@ htmlUrl: {htmlUrl}")
    
    
    message = ""
    
    if len(reviewerIds) > 0:
        for reviewerId in reviewerIds:
            message += f"<@{reviewerId}>"
        
        message += "\n"
    
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


