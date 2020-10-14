import requests
from .config import config_value

class Github:
    def __init__(self):
        self.token = config_value('github', 'token')
        self.user = config_value('github', 'user')
        self.email = config_value('github', 'email')
        self.name = config_value('github', 'name')

    # https://docs.github.com/en/rest/reference/repos#list-repositories-for-the-authenticated-user
    def repositories(self):
        url = 'https://api.github.com/user/repos'
        params = {
            'accept': 'application/vnd.github.v3+json',
            'affiliation': 'owner'
        }

        response = requests.get(url=url, params=params, auth=(self.email, self.token))
        if (response.status_code != 200):
            return None

        data = response.json()

        repos = dict()
        for repo in data:
            repos[repo['name']] = repo['clone_url']

        return repos

    # https://docs.github.com/en/rest/reference/repos#create-a-repository-for-the-authenticated-user
    def repositoryCreate(self, name, description):
        url = 'https://api.github.com/user/repos'
        params = {
            'accept': 'application/vnd.github.v3+json',
        }
        json = {
            'name': name,
            'description': description,
            'private': True
        }

        response = requests.post(url=url, params=params, auth=(self.email, self.token), json=json)
        if (response.status_code != 201):
            return None

        return response.json()['clone_url']

    # https://docs.github.com/en/rest/reference/migrations#start-an-import
    def importStart(self, gitlabRepoUrl, githubRepoName):
        url = f'https://api.github.com/repos/{self.user}/{githubRepoName}/import'
        params = {
            'accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        json = {
            'vcs_url': gitlabRepoUrl,
            'vcs': 'git',
            'vcs_username': config_value('gitlab', 'email'),
            'vcs_password': config_value('gitlab', 'token')
        }
        
        response = requests.put(url=url, params=params, auth=(self.email, self.token), json=json)
        
        if (response.status_code != 201):
            return None

        return response.json()

    # https://docs.github.com/en/rest/reference/migrations#get-an-import-status
    def importStatus(self, githubRepoName):
        url = f'https://api.github.com/repos/{self.user}/{githubRepoName}/import'
        params = {
            'accept': 'application/vnd.github.v3+json'
        }

        response = requests.get(url=url, params=params, auth=(self.email, self.token))
        if (response.status_code != 200):
            return None

        return response.json()['status']

    # https://docs.github.com/en/rest/reference/migrations#cancel-an-import
    def importCancel(self, githubRepoName):
        url = f'https://api.github.com/repos/{self.user}/{githubRepoName}/import'
        params = {
            'accept': 'application/vnd.github.v3+json'
        }

        response = requests.delete(url=url, params=params, auth=(self.email, self.token))
        if (response.status_code != 204):
            return None

        return True

    # https://docs.github.com/en/rest/reference/migrations#get-commit-authors
    def getCommitAuthors(self, githubRepoName):
        url = f'https://api.github.com/repos/{self.user}/{githubRepoName}/import/authors'
        params = {
            'accept': 'application/vnd.github.v3+json'
        }

        response = requests.get(url=url, params=params, auth=(self.email, self.token))
        if (response.status_code != 200):
            return None

        data = response.json()
        print(data)

        authors = list()
        for author in data:
            authors.append(author['id'])

        return authors

    # https://docs.github.com/en/rest/reference/migrations#map-a-commit-author
    def mapAuthor(self, githubRepoName, authorId):
        url = f'https://api.github.com/repos/{self.user}/{githubRepoName}/import/authors/{authorId}'
        params = {
            'accept': 'application/vnd.github.v3+json'
        }
        json = {
            'email': self.email,
            'name': self.name
        }

        response = requests.patch(url=url, params=params, auth=(self.email, self.token), json=json)
        if (response.status_code != 200):
            return None

        return response.json()

    # https://docs.github.com/en/rest/reference/migrations#get-large-files
    def getLargeFiles(self, githubRepoName):
        url = f'https://api.github.com/repos/{self.user}/{githubRepoName}/import/large_files'
        params = {
            'accept': 'application/vnd.github.v3+json'
        }

        response = requests.get(url=url, params=params, auth=(self.email, self.token))
        if (response.status_code != 200):
            return None

        return response.json()

    # https://docs.github.com/en/rest/reference/migrations#update-git-lfs-preference
    def lfsPreference(self, githubRepoName):
        url = f'https://api.github.com/repos/{self.user}/{githubRepoName}/import/lfs'
        params = {
            'accept': 'application/vnd.github.v3+json'
        }
        json = {
            'use_lfs': 'opt_in'
        }

        response = requests.patch(url=url, params=params, auth=(self.email, self.token), json=json)
        if (response.status_code != 200):
            return None

        return response.json()
