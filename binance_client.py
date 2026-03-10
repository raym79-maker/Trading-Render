import os
import ccxt

class BinanceClient:
    def __init__(self):
        # Corregido el error de paréntesis que causó el Deploy Failed
        api_key = os.environ.get('BINANCE_API_KEY', '').strip()
        api_secret = os.environ.get('BINANCE_API_SECRET', '').strip()
        
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'}
        })
        # Activamos el modo demo
        self.exchange.set_sandbox_mode(True)

    def get_price(self, symbol):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

    def get_balance(self):
        balance = self.exchange.fetch_balance()
        return balance['total'].get('USDT', 0)

    def place_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side.lower(), amount)
