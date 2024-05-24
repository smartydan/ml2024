import requests
import os

token = "it dissapeared:("
languages = {'C++': 'cpp', 'yaml': 'yaml', 'bash': 'sh', 'markdown': 'md', 'C': 'c', 
             'kotlin': 'kt', 'haskell': 'hs', 'text': 'txt', 'java': 'java', 'javascript': 'js', 'python': 'py'}
extensions = tuple(['.' + el for el in languages.values()])
counts = {'C++': 0, 'yaml': 0, 'bash': 0, 'markdown': 0, 'C': 0, 'kotlin': 0,
      'haskell': 0, 'text': 0, 'java': 0, 'javascript': 0, 'python': 0}
extol = {'cpp': 'C++', 'yaml': 'yaml', 'sh': 'bash', 'md': 'markdown', 'c': 'C', 
             'kt': 'kotlin', 'hs': 'haskell', 'txt': 'text', 'java': 'java',  'js': 'javascript', 'py': 'python'}
base_dir = "..\\data\\files"


def search_github_repos(language, per_page=10):
    url = f"https://api.github.com/search/repositories?q=language:{language}&per_page={per_page}&page=6"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['items']
    return []

headers = {'Authorization': 'token ' + str(token)}

def download_file(url, destination):
    url, branch = url.split('?ref=')
    url = url.replace("api.github.com/repos", "raw.githubusercontent.com").replace("/contents/", f"/{branch}/")

    file_name, file_extension = os.path.splitext(destination)
    if file_extension not in extensions:
        print(f"Some error with extentions, file {file_name + file_extension}")
        return
    
    lang = extol[file_extension[1:]]
    if counts[lang] >= 100:
        print(f"limit execeeded on {lang}")
        return
    
    counts[lang] += 1

    if os.path.exists(destination):
        return
    
    count = 2
    while os.path.exists(destination):
        destination = f"{file_name}{count}{file_extension}"
        count += 1
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(destination, 'xb') as f:
                f.write(response.content)
            print(f"File saved: {destination}")
        else:
            print(f"Failed to download file: {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading file: {url}. {e}")

def get_repository_contents(owner, repo, path='', depth = 0):
    if (depth > 8):
        return
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    print(f"parsing {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file':
                if item['name'].endswith(extensions):
                    file_url = item['url']
                    file_name = os.path.basename(file_url)[:-11]
                    destination = os.path.join(base_dir, file_name)
                    download_file(file_url, destination)
            elif item['type'] == 'dir':
                get_repository_contents(owner, repo, item['path'], depth + 1)
        return
    print(f"Failed to retrieve repository contents. Status code: {response.status_code}")

if __name__ == "__main__":
    os.makedirs(base_dir, exist_ok=True)
    for language in languages:
        print(language)
        repos = search_github_repos(language)
        for repo in repos:
            owner = repo['owner']['login']
            repo_name = repo['name']
            print(f"Searching files in {owner}/{repo_name}")
            get_repository_contents(owner, repo_name)