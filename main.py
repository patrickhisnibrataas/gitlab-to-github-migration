import sys
import time
from src.github import Github
from src.gitlab import Gitlab

def exit(message):
    print(message)
    sys.exit()

if __name__ == "__main__":    
    # Get all gitlab repositories
    gitlab = Gitlab()    
    gitlab_repos = gitlab.repositories()
    if gitlab_repos == None:
        exit('Not able to retreive gitlab repositories')
    elif gitlab_repos == dict():
        exit('Zero repositories was fetched from the gitlab account')

    print ('Gitlab repositories found: ' + str(len(gitlab_repos)))

    # Get all github repositories
    github = Github()
    github_repos = github.repositories()
    if github_repos == None:
        exit('Not able to retreive github repositories')

    print ('Github repositories found: ' + str(len(github_repos)))
    
    # Skip repositories that already exists on github
    for key in github_repos.keys():
        alternativeKey = str(key).replace('-', ' ')
        if key in gitlab_repos.keys():
            gitlab_repos.pop(key)
            print(f'Repository "{key}" already exsists on Github and will not be exported from gitlab')
        if alternativeKey in gitlab_repos.keys():
            gitlab_repos.pop(alternativeKey)
            print(f'Repository "{alternativeKey}" already exsists on Github and will not be exported from gitlab')

    for name, url in gitlab_repos.items():
        name = str(name).replace(' ', '-')
        print(f'Starting import of repository: {name}')
        
        # Create repository that does not exist
        if github.repositoryCreate(name, '') == None:
            print(f'Unable to create repository: {name}')
            continue

        # Start import to repository
        if github.importStart(url, name) == None:
            exit(f'Unable to start import of "{url}" to github repo named "{name}"')

        # Check if import is done
        status = ''
        previousStatus = ''
        finishedStatus = [
            'complete',
            'auth_failed',
            'error',
            'detection_needs_auth',
            'detection_found_nothing',
            'detection_found_multiple',
            None
            ]

        while status not in finishedStatus:
            status = github.importStatus(name)
            if previousStatus != status:
                print(f'Status: {status}')
                previousStatus = status
            if status == 'importing':
                # Enable transfer of git lfs files
                if github.getLargeFiles(name) == None:
                    exit(f'Unable to get list of git lfs files in repo: {name}')

                if github.lfsPreference(name) == None:
                    exit(f'Unable to set git lfs preference on: {name}')
            time.sleep(1)

        if status != 'complete':
            exit(f'Import of "{name}" to Github finished with status: {status}')
        
        print(f'Import of "{name}" to Github finished with status: {status}')
