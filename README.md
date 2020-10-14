# Gitlab to Github repository migration
This python application fetches all of your Gitlab repositories and mirrors them to Github.

## Github personal access token permissions
For this application to run properly the `repo` and `admin:repo_hook` permissions must be granted to the personal access token. If this does not work, create one with all/more permissions.

## Gitlab personal access token permissions
For this application to run properly the `read_repository`, `read_user` and `read_api` permissions must be granted to the personal access token. If this does not work, create one with all/more permissions.

## Configuration
Before launching the application the `config.ini` file must be filled out. Use the `config.ini.example` file as your starting point and rename it to `config.ini`.

## How to run the application
Install dependencies found in `requirements.txt`.

Run application by starting `main.py`.

Start execution of the application by opening the url `http://127.0.0.1:5000`.
