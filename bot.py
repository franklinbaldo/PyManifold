#%%
import pymanifold as mf

import getpass

import time

# %%
username, api_key = mf.credentials.get_credentials()
client = mf.ManifoldClient(api_key)
# %%

#%%
probabilities = {
    "https://manifold.markets/FranklinBaldo/will-lula-da-silva-win-the-2022-bra": 0.75,
    "https://manifold.markets/FranklinBaldo/lula-vai-ser-eleito-presidente-do-b": 0.75,
    "https://manifold.markets/FranklinBaldo/this-market-resolves-yes-except-if": 0.95,
    "https://manifold.markets/ZhaoNan/will-lula-da-silva-win-the-2022-pre": 0.75,
    "https://manifold.markets/ManifoldMarkets/will-jair-bolsonaro-be-reelected-pr": 0.25,
    "https://manifold.markets/FranklinBaldo/this-market-resolves-yes-if-it-hits": 0.5,
}


def arbitraging(m1_url, m2_url):
    mkt1 = client.get_market_by_url(m1_url)
    mkt2 = client.get_market_by_url(m2_url)
    if abs(mkt1.probability - mkt2.probability) > 0.02:
        print("Probabilities separated by more than 2%---arbitraging!")
        if mkt1.probability > mkt2.probability:
            mkt1, mkt2 = mkt2, mkt1
        # Buy some YES from mkt1; buy some NO from mkt2
        bet_id1 = client.create_bet(mkt1.id, 1, "YES")
        bet_id2 = client.create_bet(mkt2.id, 1, "NO")
        print(bet_id1, bet_id2)
    else:
        print("no arbitrage needed")


def main():
    from pymanifold.credentials import get_credentials

    username, api_key = get_credentials()
    while True:
        for market_url in probabilities:
            subjective_prob = probabilities[market_url]
            print(market_url, subjective_prob)
            market = client.get_market_by_url(market_url)
            user = client.get_user(username)
            balance = int(user.balance)
            amount, outcome = mf.utils.kelly_calc(market, subjective_prob, balance)
            if amount > 5:
                bet_id = client.create_bet(market.id, amount, outcome)
                print("betting", amount, outcome, bet_id)
            else:
                print("not betting")
        secs = 360
        print("aguardando", secs, "segundos")
        time.sleep(secs)


if __name__ == "__main__":
    main()

    # %%
