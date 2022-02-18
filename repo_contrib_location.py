import requests
import json
import re

def fetch_user_token(client_id, client_secret):

    """
    https://docs.github.com/en/enterprise-server@3.4/rest/reference/oauth-authorizations#create-a-new-authorization
    get_url = "https://github.com/login/oauth/authorize?client_id=<your-client_id>&scopes=repo%20write:org&state=something-random"
    post_url = "POST https://github.com/login/oauth/access_token?client_id=<your-client_id>&client_secret=<your-client_secret>&code=<code-from-github>"
    """
    pass

def fetch_contributors(user, repo):
    """
    https://docs.github.com/en/rest/reference/search#search-users
    """
    url = f'https://api.github.com/repos/{user}/{repo}/contributors'
    headers = {'Accept': 'application/vnd.github.v3+json'}

    response = requests.get(url, headers=headers)

    users_dict = response.json()
    usernames = []
    for user in users_dict:
        username = user['login']
        usernames.append(username)

    return usernames

def fetch_users_by_location(usernames=list, locations=list):
    """
    https://docs.github.com/en/rest/reference/search#search-users Rate-limits
    apply over github api.
    """
    contributors = []
    for user in usernames:
        url = f'https://github.com/{user}'
        response = requests.get(url)
        location_match = re.search('p-label\"\>(.*)\<\/span\>', response.text)
        if location_match:
            user_location = location_match.groups()[0].lower()
        locations = [ location.lower() for location in locations ]
        if user_location in locations:
            contributors.append(user)

    return contributors


if __name__ == "__main__":

    user = "k8ssandra"
    repo = "k8ssandra"
    auth_user = "RoachMJ"
    usernames = fetch_contributors(user, repo)
    users = fetch_users_by_location(usernames, locations)
    # users = fetch_users_by_location(usernames, locations, auth_user, auth_token)
    print(users)



