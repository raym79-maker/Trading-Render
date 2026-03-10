import os
import ccxt

class BinanceClient:
    def __init__(self):
        api_key = os.environ.get('BINANCE_API_KEY', '').strip()
        api_secret = os.environ.get('BINANCE_API_SECRET', '').strip()
        
        # Usamos el proxy de España para evitar el bloqueo regional de Render
        proxy_url = "http://oorqsbda:vu935t81ybpq@64.137.96.74:6641"

        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'proxies': {
                'http': proxy_url,
                'https': proxy_url,
            },
            'options': {
                'defaultType': 'future', # CAMBIO A FUTUROS
            }
        })
        # Activamos el modo demo para Futuros
        self.exchange.set_sandbox_mode(True)

    def get_price(self, symbol):
        # En futuros los símbolos suelen ser 'BTC/USDT:USDT' o 'BTCUSDT'
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

    def get_balance(self):
        # El balance de futuros se consulta distinto al de spot
        balance = self.exchange.fetch_balance()
        # Buscamos el saldo en la billetera de futuros
        return balance['total'].get('USDT', 0)

    def place_order(self, symbol, side, amount):
        # Las órdenes de futuros requieren parámetros adicionales a veces, 
        # pero para una orden de mercado básica esto sirve:
        return self.exchange.create_market_order(symbol, side.lower(), amount)
