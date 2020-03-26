import requests

url_followers = 'https://api.github.com/users/{}/followers'
url_following = 'https://api.github.com/users/{}/following'
url_id = 'https://api.github.com/users/{}'

gh_session = requests.Session()


def init_session(github_username, github_token):
    gh_session.auth = (github_username, github_token)


def get_user_followers(user):
    rtn = gh_session.get(url=url_followers.format(user))
    if rtn.status_code != 200:
        print("Error! Status: " + str(rtn.status_code))
        return
    data = rtn.json()
    return data


def get_user_following(user):
    rtn = gh_session.get(url=url_following.format(user))
    if rtn.status_code != 200:
        print("Error! Status: " + str(rtn.status_code))
        return
    data = rtn.json()
    return data


def get_user_id(user):
    rtn = requests.get(url=url_id.format(user))
    if rtn.status_code != 200:
        print("Error! Status: " + str(rtn.status_code))
        return
    data = rtn.json()
    return data['id']
