import requests

def make_headers(
    client_id,
    reddit_app_private_key,
    account_username,
    account_password,
):
    auth = requests.auth.HTTPBasicAuth(client_id, reddit_app_private_key)
    data = {
        "grant_type": "password",
        "username": account_username,
        "password": account_password,
    }

    headers = {"User-Agent": "MyAPI/0.0.1"}

    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )

    token = res.json()["access_token"]
    headers["Authorization"] = f"bearer {token}"

    reddit_app_private_key = account_password = data = ""
    assert reddit_app_private_key == account_password == data == ""

    return headers
