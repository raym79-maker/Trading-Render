import os
import ccxt

class BinanceClient:
    def __init__(self):
        # 1. Capturamos las llaves de la Testnet desde Render
        api_key = str(os.environ.get('BINANCE_API_KEY', '')).strip()
        api_secret = str(os.environ.get('BINANCE_API_SECRET', '')).strip()
        
        # Log para verificar que Render las entrega
        print(f"--- MODO TESTNET ACTIVO ---")
        print(f"API Key Demo: {api_key[:4]}...{api_key[-4:]}")
        
        # 2. Configuración del Proxy de España
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

        # 3. ACTIVAR MODO DEMO (Sandbox)
        # Esto hace que el bot use los servidores de prueba de Binance
        self.exchange.set_sandbox_mode(True)

    def get_price(self, symbol):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

    def get_balance(self):
        # En la Testnet, Binance te regala fondos ficticios para probar
        balance = self.exchange.fetch_balance()
        return balance['total'].get('USDT', 0)

    def place_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side.lower(), amount)
