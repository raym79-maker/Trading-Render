import os
import ccxt

class BinanceClient:
    def __init__(self):
        # Capturamos las llaves
        api_key = os.environ.get('BINANCE_API_KEY', '').strip()
        api_secret = os.environ.get('BINANCE_API_SECRET', '').strip()
        
        # LOG DE DEPURACIÓN (Seguro)
        if not api_key or not api_secret:
            print("ERROR CRÍTICO: Las variables de entorno están VACÍAS en Render.")
        else:
            # Imprime longitud y los extremos para que tú mismo verifiques
            print(f"DEBUG: API Key recibida. Longitud: {len(api_key)} caracteres.")
            print(f"DEBUG: Empieza con '{api_key[:4]}' y termina con '{api_key[-4:]}'")

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
            # Forzamos a que use la API de Binance.com explícitamente
            'urls': {
                'api': {
                    'public': 'https://api.binance.com/api/v3',
                    'private': 'https://api.binance.com/api/v3',
                }
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
