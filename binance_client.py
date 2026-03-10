import os
import ccxt

class BinanceClient:
    def __init__(self):
        api_key = os.environ.get('BINANCE_API_KEY', '').strip()
        api_secret = os.environ.get('BINANCE_API_SECRET', '').strip()
        
        proxy_url = "http://oorqsbda:vu935t81ybpq@64.137.96.74:6641"

        # Configuramos CCXT para que sea NATIVO de Futuros desde el inicio
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'proxies': {
                'http': proxy_url,
                'https': proxy_url,
            },
            'options': {
                'defaultType': 'future', # Esto cambia las URLs base automáticamente
            }
        })
        
        # Activamos el modo sandbox de forma que CCXT maneje los endpoints de Futuros
        self.exchange.set_sandbox_mode(True)

    def get_price(self, symbol):
        # Limpiamos símbolo: BTC/USDT -> BTCUSDT
        clean_symbol = symbol.replace('/', '').split(':')[0]
        # Usamos el método estándar de CCXT que ya sabe manejar Futuros
        ticker = self.exchange.fetch_ticker(clean_symbol)
        return float(ticker['last'])

    def get_balance(self):
        # fapiPrivateGetBalance a veces falla por el método GET en Testnet
        # fetch_balance es más robusto porque CCXT elige el mejor endpoint
        balance = self.exchange.fetch_balance()
        return float(balance['total'].get('USDT', 0))

    def place_order(self, symbol, side, amount):
        clean_symbol = symbol.replace('/', '').split(':')[0]
        return self.exchange.create_market_order(clean_symbol, side.upper(), amount)
