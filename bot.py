import os
import ccxt
from dotenv import load_dotenv

load_dotenv()

class BinanceClient:
    def __init__(self):
        # Elegimos el proxy de España de tu lista de Webshare
        proxy_url = "http://oorqsbda:vu935t81ybpq@64.137.96.74:6641"

        self.exchange = ccxt.binance({
            'apiKey': os.getenv('BINANCE_API_KEY'),
            'secret': os.getenv('BINANCE_API_SECRET'),
            'enableRateLimit': True,
            'proxies': {
                'http': proxy_url,
                'https': proxy_url,
            },
            'options': {
                'defaultType': 'spot',
            }
        })
    # ... el resto de tus funciones (get_balance, etc) se mantienen igual

def ejecutar_ciclo(objetivo_compra=95000):
    try:
        logging.info("Iniciando ciclo de verificación...")
        
        # Obtenemos datos del mercado
        saldo = client.get_balance()
        precio = client.get_price("BTCUSDT")
        
        logging.info(f"Saldo: {saldo} USDT | Precio BTC: {precio} USDT")
        
        # Aquí la indentación debe ser exacta (usualmente 8 espacios respecto al inicio)
        if precio <= objetivo_compra:
            logging.warning(f"¡Precio {precio} <= {objetivo_compra}! Ejecutando orden de compra...")
            try:
                # Calculamos una cantidad que sume al menos 105 USDT para estar seguros
                cantidad_calculada = round(105 / precio, 3) 
                orden = client.place_order("BTCUSDT", "BUY", str(cantidad_calculada))
                logging.info(f"Orden ejecutada: {cantidad_calculada} BTC. ID: {orden['orderId']}")
            except Exception as e:
                logging.error(f"Fallo al ejecutar la compra: {e}")
        else:
            logging.info(f"El precio se mantiene por encima del objetivo ({objetivo_compra}).")
            
    except Exception as e:
        logging.error(f"Error en el ciclo de ejecución: {e}")

if __name__ == "__main__":

    ejecutar_ciclo()
