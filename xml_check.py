import os
import requests
import sys
import logging

# ログの出力先のファイルを指定
#logging.basicConfig(filename='test.log', level=logging.DEBUG)

tokenGithub:str = "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"

def main():
    pr_number = sys.argv[1]
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {tokenGithub}"
    }
    
    pr_url = f"{os.environ['GITHUB_API_URL']}/repos/{os.environ['GITHUB_REPOSITORY']}/pulls/{pr_number}"
    print(f"pr_url: {pr_url}")
    
    pr_response = requests.get(pr_url, headers=headers)
    print(f"pr_response: {pr_response}")
    
    pr_response_json = pr_response.json()
    print(f"pr_response_json: {pr_response_json}")
    
    files_url = pr_response_json['url'] + "/files"
    print(f"files_url: {files_url}")
    
    files_response = requests.get(files_url, headers=headers)
    print(f"files_response: {files_response}")
    
    files_response_json = files_response.json()
    print(f"files_response_json: {files_response_json}")

    # Check if any XML files are present in the pull request
    for file in files_response_json:
        if file['filename'].endswith('.xml'):
            print(f"XML file found in {file['filename']}")
            sys.exit(1)

if __name__ == '__main__':
    main()
