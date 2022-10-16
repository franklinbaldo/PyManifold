import os

import keyring
# %%
MANIFOLD_USERNAME = os.environ.get('MANIFOLD_USERNAME') or keyring.get_password('manifold.markets', 'MANIFOLD_USERNAME')
MANIFOLD_APIKEY = os.environ.get('MANIFOLD_APIKEY') or keyring.get_password('manifold.markets', 'MANIFOLD_APIKEY')


def set_credentials(username, api_key):
    assert all([username,api_key]),'you should insert a valid username and api_key'

    keyring.set_password('manifold.markets', 'MANIFOLD_USERNAME', username)
    keyring.set_password('manifold.markets','MANIFOLD_APIKEY', api_key)
    os.environ['MANIFOLD_USERNAME']=username
    os.environ['MANIFOLD_APIKEY'] = api_key


def get_credentials():
    username = os.environ.get('MANIFOLD_USERNAME') or keyring.get_password('manifold.markets', 'MANIFOLD_USERNAME')
    api_key = os.environ.get('MANIFOLD_APIKEY') or keyring.get_password('manifold.markets', 'MANIFOLD_APIKEY')
    try:
        assert all([username,api_key]), 'set your api key using environ or keyring'
    except AssertionError:
        username = input('MANIFOLD_USERNAME')
        api_key = input('MANIFOLD_APIKEY')
        set_credentials(username,api_key)
    return username, api_key

