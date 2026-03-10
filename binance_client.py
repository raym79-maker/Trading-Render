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
        # Forzamos la URL de la Testnet de Futuros
        self.exchange.urls['api']['fapiPublic'] = 'https://testnet.binancefuture.com/fapi/v1'
        self.exchange.urls['api']['fapiPrivate'] = 'https://testnet.binancefuture.com/fapi/v1'

    def get_price(self, symbol):
        # Limpiamos el símbolo para futuros (ej: de BTC/USDT a BTCUSDT)
        clean_symbol = symbol.replace('/', '').split(':')[0]
        ticker = self.exchange.fapiPublicGetTickerPrice({'symbol': clean_symbol})
        return float(ticker['price'])

    def get_balance(self):
        # Cambiamos fapiPrivateGetAccount por fapiPrivateGetBalance
        balances = self.exchange.fapiPrivateGetBalance()
        for item in balances:
            if item['asset'] == 'USDT':
                return float(item['balance'])
        return 0.0

    def place_order(self, symbol, side, amount):
        clean_symbol = symbol.replace('/', '').split(':')[0]
        return self.exchange.fapiPrivatePostOrder({
            'symbol': clean_symbol,
            'side': side.upper(),
            'type': 'MARKET',
            'quantity': amount
        })
