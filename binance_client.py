import os
import ccxt

class BinanceClient:
    def __init__(self):
        # 1. Limpieza de llaves
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
                'defaultType': 'future', 
            }
        })
        
        # Forzamos las URLs de la Testnet de Futuros de forma manual
        self.exchange.urls['api']['fapiPublic'] = 'https://testnet.binancefuture.com/fapi/v1'
        self.exchange.urls['api']['fapiPrivate'] = 'https://testnet.binancefuture.com/fapi/v1'

    def get_price(self, symbol):
        # Limpiamos el símbolo (ej: de BTC/USDT a BTCUSDT)
        clean_symbol = symbol.replace('/', '').split(':')[0]
        # Usamos la llamada directa al ticker de precios de futuros
        ticker = self.exchange.fapiPublicGetTickerPrice({'symbol': clean_symbol})
        return float(ticker['price'])

    def get_balance(self):
        # SOLUCIÓN AL ERROR -5000:
        # Usamos fapiPrivateGetAccount, que es el endpoint más estable en Testnet
        account_info = self.exchange.fapiPrivateGetAccount()
        # Buscamos el saldo disponible en USDT dentro de la cuenta de futuros
        for asset in account_info['assets']:
            if asset['asset'] == 'USDT':
                return float(asset['walletBalance'])
        return 0.0

    def place_order(self, symbol, side, amount):
        clean_symbol = symbol.replace('/', '').split(':')[0]
        return self.exchange.create_market_order(clean_symbol, side.upper(), amount)
