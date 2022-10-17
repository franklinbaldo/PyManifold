import os
import typing as t
from dotenv import load_dotenv
from pathlib import Path

# %%


def set_credentials(username, api_key):
    assert all([username, api_key]), "you should insert a valid username and api_key"
    os.environ["MANIFOLD_USERNAME"] = username
    os.environ["MANIFOLD_APIKEY"] = api_key


def get_credentials(dotenv_path=None):
    if dotenv_path:
        load_dotenv(Path(dotenv_path))

    username = os.environ.get("MANIFOLD_USERNAME")
    api_key = os.environ.get("MANIFOLD_APIKEY")
    if not all([username, api_key]):
        try:
            username, api_key = get_credentials(dotenv_path=Path.cwd() / ".env")
        except Exception as e:
            print("error loading dotenv")
    assert all(
        [username, api_key]
    ), "you should set variables MANIFOLD_USERNAME and MANIFOLD_APIKEY on your enviroment"
    return username, api_key
