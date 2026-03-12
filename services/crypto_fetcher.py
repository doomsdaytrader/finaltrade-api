import requests
from sqlalchemy.orm import Session
from models import Price

COINS = ["bitcoin", "ethereum", "solana", "binancecoin", "terra-luna", "terrausd"]

def fetch_prices(db: Session):
    try:
        coin_ids = ",".join(COINS)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies=usd"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            for coin in COINS:
                if coin in data:
                    price_val = data[coin]["usd"]
                    # check if current price for today exists or just insert new row
                    new_price = Price(
                        coin_id=coin,
                        price_usd=price_val
                    )
                    db.add(new_price)
            db.commit()
    except Exception as e:
        print(f"Error fetching prices: {e}")
