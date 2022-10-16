import os

import keyring

# %%
MANIFOLD_USERNAME = os.environ.get("MANIFOLD_USERNAME")
MANIFOLD_APIKEY = os.environ.get("MANIFOLD_APIKEY")


def set_credentials(username, api_key):
    assert all([username, api_key]), "you should insert a valid username and api_key"
    os.environ["MANIFOLD_USERNAME"] = username
    os.environ["MANIFOLD_APIKEY"] = api_key


def get_credentials():
    username = os.environ.get("MANIFOLD_USERNAME")
    api_key = os.environ.get("MANIFOLD_APIKEY")
    assert all([username, api_key]), "set your api key using environ"
    return username, api_key
