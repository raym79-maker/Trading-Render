import os
import ccxt
# Eliminamos la carga de .env para que Render use sus propias variables
# from dotenv import load_dotenv 
# load_dotenv()

class BinanceClient:
    def __init__(self):
        # Obtenemos las llaves directamente del sistema (Render)
        api_key = os.environ.get('BINANCE_API_KEY')
        api_secret = os.environ.get('BINANCE_API_SECRET')
        
        # Validación rápida para ver en logs si las llaves llegaron (sin mostrarlas completas)
        if not api_key or not api_secret:
            print("ERROR: No se detectaron las API Keys en las variables de entorno.")
        else:
            print(f"API Key detectada (empieza con: {api_key[:5]}...)")

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
                'defaultType': 'spot',
            }
        })
    
    # ... el resto de funciones (get_balance, etc) igual
