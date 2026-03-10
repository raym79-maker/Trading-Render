import os
import ccxt

class BinanceClient:
    def __init__(self):
        # 1. Limpieza de variables (quitamos espacios accidentales)
        api_key = str(os.environ.get('BINANCE_API_KEY', '')).strip()
        api_secret = str(os.environ.get('BINANCE_API_SECRET', '')).strip()
        
        # 2. LOG CRÍTICO (Para que tú veas qué está leyendo Render)
        print(f"--- DIAGNÓSTICO DE INICIO ---")
        print(f"Longitud API Key: {len(api_key)}")
        print(f"Empieza con: {api_key[:4]} | Termina con: {api_key[-4:]}")
        
        # Proxy de España
        proxy_url = "http://oorqsbda:vu935t81ybpq@64.137.96.74:6641"

        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'proxies': {
                'http': proxy_url,
                'https': proxy_url,
            },
            'options': {'defaultType': 'spot'}
        })

    def get_price(self, symbol):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

    def get_balance(self):
        # Intentamos obtener el balance para probar la conexión privada
        balance = self.exchange.fetch_balance()
        return balance['total']['USDT']

    def place_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side.lower(), amount)
