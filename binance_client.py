import os
import ccxt

class BinanceClient:
    def __init__(self):
        # 1. Limpieza total de llaves
        api_key = os.environ.get('BINANCE_API_KEY', '').strip()
        api_secret = os.environ.get('BINANCE_API_SECRET', '').strip()
        
        # Proxy de España (Madrid)
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
                'defaultType': 'future', # Definimos Futuros
            },
            'urls': {
                'api': {
                    'fapiPublic': 'https://testnet.binancefuture.com/fapi/v1',
                    'fapiPrivate': 'https://testnet.binancefuture.com/fapi/v1',
                }
            }
        })

    def get_price(self, symbol):
        # Para futuros de Binance, usa 'BTCUSDT' (sin barra)
        ticker = self.exchange.fapiPublicGetTickerPrice({'symbol': symbol.replace('/', '')})
        return float(ticker['price'])

    def get_balance(self):
        # En futuros Testnet, se usa fapiPrivateGetAccount
        balance = self.exchange.fapiPrivateGetAccount()
        for asset in balance['assets']:
            if asset['asset'] == 'USDT':
                return float(asset['walletBalance'])
        return 0.0

    def place_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side.lower(), amount)
