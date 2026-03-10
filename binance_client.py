import os
import ccxt
from dotenv import load_dotenv

# Cargamos las variables de entorno desde el archivo .env o del sistema
load_dotenv()

class BinanceClient:
    def __init__(self):
        # Inicializamos el cliente de Binance con tus credenciales
        self.exchange = ccxt.binance({
            'apiKey': os.getenv('BINANCE_API_KEY'),
            'secret': os.getenv('BINANCE_API_SECRET'),
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot', # Asegúrate de que esto coincida con lo que operas
            }
        })

    def get_balance(self):
        """Devuelve el saldo disponible en USDT"""
        balance = self.exchange.fetch_balance()
        return balance['total']['USDT']

    def get_price(self, symbol):
        """Devuelve el precio actual de mercado para un símbolo (ej: BTCUSDT)"""
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['last']

    def place_order(self, symbol, side, amount):
        """Ejecuta una orden de mercado"""
        # side debe ser 'buy' o 'sell'
        return self.exchange.create_market_order(symbol, side.lower(), amount)