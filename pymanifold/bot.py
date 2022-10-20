import os
import typing as t
from pathlib import Path
from dotenv import dotenv_values
from .lib import ManifoldClient
from abc import abstractmethod
# %%


class Strategy:
    name: str

    @abstractmethod
    def run(bot):
        pass


class Bot:
    client: ManifoldClient
    username: str = None
    strategies: t.List[Strategy] = []
    SLEEP_TIME: int = 360
    RUN_ONCE: bool = True

    def __init__(self, dotenv_path=None, username=None, api_key=None):
        env = dotenv_values(dotenv_path=dotenv_path) if dotenv_path else os.environ
        self.username = username or env.get("MANIFOLD_USERNAME")
        api_key = api_key or env.get("MANIFOLD_APIKEY")
        if not all([username, api_key]):
            print("you should set bot api_key and username before using it")
        self.client = ManifoldClient(api_key)

    def my_balance(self):
        return self.client.get_user(self.username).balance

    def run(self, run_once=RUN_ONCE, sleep_time=SLEEP_TIME, min_balance=10):
        for strategy in self.strategies:
            balance= self.my_balance()
            print(strategy.name)
            print(f"Balance: {balance}")
            if balance < min_balance:
                print(f'you need at least M${min_balance} to run this strategy, skipping')
                break
            strategy.run(self)
        if run_once:
            return
        else:
            sleep(self._sleep_time)
            self.run(run_once=run_once, sleep_time=sleep_time)
