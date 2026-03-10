import os
import ccxt
from dotenv import load_dotenv

load_dotenv()

class BinanceClient:
    def __init__(self):
        # Usando tu proxy de España (Madrid) de Webshare
        proxy_url = "http://oorqsbda:vu935t81ybpq@64.137.96.74:6641"

        self.exchange = ccxt.binance({
            'apiKey': os.getenv('BINANCE_API_KEY'),
            'secret': os.getenv('BINANCE_API_SECRET'),
            'enableRateLimit': True,
            'proxies': {
                'http': proxy_url,
                'https': proxy_url,
            },
            'options': {
                'defaultType': 'spot',
            }
        })

    def get_balance(self):
        balance = self.exchange.fetch_balance()
        return balance['total']['USDT']

    def get_price(self, symbol):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

    def place_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side.lower(), amount)
