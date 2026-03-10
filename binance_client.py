import os
import ccxt

class BinanceClient:
    def __init__(self):
        # Leemos las variables directamente del sistema de Render
        api_key = os.environ.get('BINANCE_API_KEY')
        api_secret = os.environ.get('BINANCE_API_SECRET')
        
        # --- VALIDACIÓN DE SEGURIDAD PARA LOGS ---
        if api_key and api_secret:
            # Esto imprimirá algo como: "Leyendo API Key: abcd...wxyz"
            print(f"INFO: API Key detectada: {api_key[:4]}...{api_key[-4:]}")
        else:
            print("ERROR: ¡No se encontraron las API Keys en Environment de Render!")

        # Tu proxy de España (Madrid)
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
        balance = self.exchange.fetch_balance()
        return balance['total']['USDT']

    def place_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side.lower(), amount)
