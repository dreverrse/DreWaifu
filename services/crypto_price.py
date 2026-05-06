import requests


COINGECKO_IDS = {
    "btc": "bitcoin",
    "bitcoin": "bitcoin",
    "eth": "ethereum",
    "ethereum": "ethereum",
    "bnb": "binancecoin",
    "sol": "solana",
    "solana": "solana",
    "xrp": "ripple",
    "ada": "cardano",
    "cardano": "cardano",
    "doge": "dogecoin",
    "dogecoin": "dogecoin",
    "dot": "polkadot",
    "matic": "matic-network",
    "avax": "avalanche-2",
    "link": "chainlink",
    "ltc": "litecoin",
    "atom": "cosmos",
    "uni": "uniswap",
    "trx": "tron",
    "near": "near",
    "icp": "internet-computer",
    "shib": "shiba-inu",
    "pepe": "pepe",
}


def resolve_coin_id(coin):
    return COINGECKO_IDS.get(coin.lower(), coin.lower())


def get_price(coin):
    coin_id = resolve_coin_id(coin)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true",
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        if coin_id not in data:
            return None, f"Coin '{coin}' tidak ditemukan."
        price = data[coin_id]["usd"]
        change = data[coin_id].get("usd_24h_change", 0)
        return {"coin": coin_id, "price": price, "change_24h": round(change, 2)}, None
    except Exception as e:
        return None, f"CRYPTO ERROR: {e}"


def get_multiple_prices(coins):
    ids = [resolve_coin_id(c) for c in coins]
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(ids),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, f"CRYPTO ERROR: {e}"
