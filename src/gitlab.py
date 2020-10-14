import requests
from .config import config_value

class Gitlab:
    def __init__(self):
        self.token = config_value('gitlab', 'token')
        self.user = config_value('gitlab', 'user')
        self.email = config_value('gitlab', 'email')

    # https://docs.gitlab.com/ee/api/projects.html#list-user-projects
    def repositories(self):
        url = 'https://gitlab.com/api/v4/users/' + self.user + '/projects?per_page=999'
        response = requests.get(url=url, headers={'PRIVATE-TOKEN': self.token})
        if (response.status_code != 200):
            return None

        data = response.json()

        repos = dict()
        for repo in data:
            repos[repo['name']] = repo['http_url_to_repo']

        return repos