from abc import abstractmethod
import os
import random
import time
import typing as t

import numpy as np
import pymanifold as mf

from pymanifold.types import LiteUser
from pymanifold.types import Market
from pymanifold.bot import Strategy
from pymanifold.lib import ManifoldClient
import scipy as sp
from dotenv import load_dotenv

load_dotenv()
RUN_ONCE = os.environ.get("RUN_ONCE", default=True)
SLEEP_TIME = os.environ.get("SLEEP_TIME", default=360)
CONFIRM_BETS = False
MAX_BACKOFF = 4


    

def shuffled(x):
    x = list(x)
    random.shuffle(x)
    return x


def cartesian_to_hyperbolic(p, y, n):
    r = y**p * n ** (1 - p)
    phi = np.log(y / r) / (1 - p)
    return r, phi


def hyperbolic_to_cartesian(p, r, phi):
    return np.exp((1 - p) * phi) * r, np.exp(-p * phi) * r


def prob_from_cartesian(p, y, n):
    return (p * n) / (p * n + (1 - p) * y)


def skip_market(m: Market):
    recent_bets = [b for b in m.bets if b.createdTime / 1000 >= time() - 60 * 60]
    if m.isResolved:
        return f'Market "{m.question}" has resolved.'
    if m.closeTime / 1000 <= time() + 60 * 60:
        return f'Market "{m.question}" closes in less then an hour.'
    if m.probability <= 0.02:
        return f'Market "{m.question}" has probability <= 2%.'
    if m.probability >= 0.98:
        return f'Market "{m.question}" has probability >= 2%.'
    return None


def get_shares(markets: t.List[Market]):

    return np.array([m.pool["YES"] for m in markets]), np.array(
        [m.pool["NO"] for m in markets]
    )


class Bot:
    client: mf.ManifoldClient
    username: LiteUser = None


    def __init__(self, dotenv_path=None, username=None, api_key=None):
        env = dotenv_values(dotenv_path=dotenv_path) if dotenv_path else os.environ
        self.username = username or env.get("MANIFOLD_USERNAME")
        api_key = api_key or env.get("MANIFOLD_APIKEY")
        if not all([username, api_key]):
            print("you should set bot api_key and username before using it")
        self.client = ManifoldClient(api_key)

    def get_balance(self):
        return self.client.get_user(self.username).balance

    def run(
        self, strategies: t.List[Strategy], run_once=RUN_ONCE, sleep_time=SLEEP_TIME
    ):
        for strategy in strategies:
            print(f"Balance: {self.get_balance()}")
            strategy.run(self)
        if run_once is False:
            time.sleep(sleep_time)
            self.run(strategies, run_once, sleep_time)
        


class Backoff:
    t = 1

    def reset(self) -> None:
        self.t = 1
        
    def should_fire(self) -> bool:
        return True


class ArbitrageGroup(Strategy):
    def __init__(self, name, d):
        self.name = name
        self.slugs, m = zip(*d.items())
        self.matrix = np.array(m).T
        self.backoff = Backoff()

    def compute_profit_outcomes(self, dy, dn):
        return self.matrix @ dy + (1 - self.matrix) @ dn

    def optimize(self, p, y, n):
        r, phi = cartesian_to_hyperbolic(p, y, n)

        def f(dphi):
            y2, n2 = hyperbolic_to_cartesian(p, r, phi + dphi)
            profit = self.compute_profit_outcomes(y - y2, n - n2)
            return -np.min(profit)

        # res = sp.optimize.minimize(f, method='CG', jac=True, x0=[-0.01, 0, 0.0263, 0, 0, 0])
        res = sp.optimize.differential_evolution(f, [(-1, 1)] * len(p))

        if res.success:
            y2, n2 = hyperbolic_to_cartesian(p, r, phi + res.x)
            profit = self.compute_profit_outcomes(y - y2, n - n2)
            return profit, y2, n2
        else:
            raise Exception(f"{res.message}" + "\n" + str(res))

    def run(self, bot: Bot):
        if not self.backoff.should_fire():
            return

        print()
        print(f"=== {self.name} ===")

        while True:
            markets: t.List[Market] = [
                bot.client.get_market_by_slug(slug) for slug in self.slugs
            ]
            for m in markets:
                if skip := skip_market(m):
                    print(skip)
                    print("Skipping group.")
                    self.backoff.reset()
                    return

            p = np.array([m.p for m in markets])
            y, n = get_shares(markets)
            print("Prior probs:    ", prob_from_cartesian(p, y, n))

            profit, y2, n2 = self.optimize(p, y, n)
            shares = n2 - n - y2 + y
            print("Posterior probs:", prob_from_cartesian(p, y2, n2))
            print("Profits:", profit)
            if np.min(profit) <= 0.01 * len(markets):
                print("Profit negligible, skipping")
                return

            for i, m in enumerate(markets):
                print(m.question)
                if shares[i] > 0.5:
                    print(f"  Buy {shares[i]} YES for M${n2[i] - n[i]}")
                elif shares[i] < -0.5:
                    print(f"  Buy {-shares[i]} NO for M${y2[i] - y[i]}")
                else:
                    print("  Do not trade")

            self.backoff.reset()

            # TODO: make sure we can afford it!

            if CONFIRM_BETS and input("Proceed? (y/n)") != "y":
                return

            # Make sure markets haven't moved
            if not np.allclose(
                (y, n),
                get_shares(
                    [bot.client.get_market_by_slug(slug) for slug in self.slugs]
                ),
            ):
                print("Markets have moved!, Skipping group.")
                return

            for i, m in shuffled(enumerate(markets)):
                if shares[i] > 0.5:
                    amount = int(n2[i] - n[i])
                    outcome = "YES"
                    if bot.get_balance()>amount:
                        bot.client.create_bet(m.id, amount, outcome)

                elif shares[i] < -0.5:
                    amount = int(y2[i] - y[i])
                    outcome = "NO"
                    if bot.get_balance()>amount:
                        bot.client.create_bet(m.id, amount, outcome)


# from private import API_KEY, USER_ID, ALL_GROUPS

if __name__ == "__main__":
    from secret_config import GROUPS
    username = os.environ.get('MANIFOLD_USERNAME')
    # from public_config import *
    strategies = [ArbitrageGroup(name, d) for name, d in GROUPS.items()]
    bot = Bot(username=username)
    bot.run(strategies)
