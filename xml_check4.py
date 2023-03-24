import os
import requests

# プルリクエストのURL
pull_request_url = os.environ['GITHUB_API_URL'] + '/repos/' + os.environ['GITHUB_REPOSITORY'] + '/pulls/' + os.environ['PR_NUMBER']
print(f"@ pull_request_url: {pull_request_url}")

# APIリクエストを送信して、変更内容を取得する
response = requests.get(pull_request_url)
print(f"@ response: {response}")

pull_request_data = response.json()
print(f"@ files: {pull_request_data['files']}")

# プルリクエストの変更内容にXMLファイルが含まれているか確認する
for file in pull_request_data['files']:
    if file['filename'].endswith('.xml'):
        print("プルリクエストでXMLファイルが変更されました")
        exit(1)

print("プルリクエストでXMLファイルは変更されていません")
exit(0)
