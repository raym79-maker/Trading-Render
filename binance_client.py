import os
import ccxt

class BinanceClient:
    def __init__(self):
        # Leemos las llaves de la Testnet de Futuros
        api_key = os.environ.get('BINANCE_API_KEY', '').strip()
        api_secret = os.environ.get('BINANCE_API_SECRET', '').strip()
        
        # Proxy de España para saltar el bloqueo regional de Render (EE.UU.)
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
                'defaultType': 'future', # Modo Futuros
            },
            'urls': {
                'api': {
                    'public': 'https://testnet.binancefuture.com/fapi/v1',
                    'private': 'https://testnet.binancefuture.com/fapi/v1',
                }
            }
        })

    # Esta es la función que falta en tus logs actuales
    def get_price(self, symbol):
        # Asegúrate que en bot.py pases el símbolo como 'BTCUSDT'
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

    def get_balance(self):
        balance = self.exchange.fetch_balance()
        # En futuros el balance se extrae del total disponible en la billetera
        return balance['total'].get('USDT', 0)

    def place_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side.lower(), amount)
