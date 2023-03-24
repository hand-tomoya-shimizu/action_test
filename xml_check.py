import os
import requests

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
    exit(1)

print("プルリクエストでXMLファイルは変更されていません")
exit(0)