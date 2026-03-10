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
            },
            'urls': {
                'api': {
                    'public': 'https://testnet.binancefuture.com/fapi/v1',
                    'private': 'https://testnet.binancefuture.com/fapi/v1',
                }
            }
        })

    # Esta es la función que te pide el error en los logs
    def get_price(self, symbol):
        # Para futuros, a veces el símbolo necesita ser BTCUSDT
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

    def get_balance(self):
        balance = self.exchange.fetch_balance()
        # En futuros, el saldo se busca en la sección 'total'
        return balance['total'].get('USDT', 0)

    def place_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side.lower(), amount)
