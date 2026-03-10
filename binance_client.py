import os
import ccxt

class BinanceClient:
    def __init__(self):
        api_key = os.environ.get('BINANCE_API_KEY', '').strip()
        api_secret = os.environ.get('BINANCE_API_SECRET', '').strip()
        
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
                'defaultType': 'future', 
            }
        })
        # Forzamos las URLs manuales de la Testnet de Futuros
        self.exchange.urls['api']['fapiPublic'] = 'https://testnet.binancefuture.com/fapi/v1'
        self.exchange.urls['api']['fapiPrivate'] = 'https://testnet.binancefuture.com/fapi/v1'

    def get_price(self, symbol):
        # Limpiamos el símbolo (ej: de BTC/USDT a BTCUSDT)
        clean_symbol = symbol.replace('/', '').split(':')[0]
        # Usamos el método específico de Futuros para el precio
        ticker = self.exchange.fapiPublicGetTickerPrice({'symbol': clean_symbol})
        return float(ticker['price'])

    def get_balance(self):
        # CAMBIO CLAVE: Usamos fapiPrivateGetBalance en lugar de Account
        # Esto soluciona el error -5000
        balances = self.exchange.fapiPrivateGetBalance()
        for item in balances:
            if item['asset'] == 'USDT':
                return float(item['balance'])
        return 0.0

    def place_order(self, symbol, side, amount):
        clean_symbol = symbol.replace('/', '').split(':')[0]
        return self.exchange.create_market_order(clean_symbol, side.upper(), amount)
