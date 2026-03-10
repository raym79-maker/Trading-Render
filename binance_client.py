import os
import ccxt

class BinanceClient:
    def __init__(self):
        # 1. Obtenemos las llaves de la Testnet de Futuros
        api_key = os.environ.get('BINANCE_API_KEY', '').strip()
        api_secret = os.environ.get('BINANCE_API_SECRET', '').strip()
        
        # 2. Proxy de España (Madrid) para saltar el bloqueo regional de Render
        proxy_url = "http://oorqsbda:vu935t81ybpq@64.137.96.74:6641"

        # 3. Configuración manual de URLs de Futuros
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'proxies': {
                'http': proxy_url,
                'https': proxy_url,
            },
            'options': {
                'defaultType': 'future', # Definimos que operaremos Futuros
            },
            'urls': {
                'api': {
                    'public': 'https://testnet.binancefuture.com/fapi/v1',
                    'private': 'https://testnet.binancefuture.com/fapi/v1',
                }
            }
        })
        
        # NOTA: NO usamos self.exchange.set_sandbox_mode(True) 
        # porque eso es lo que causa el error en los logs actuales.
