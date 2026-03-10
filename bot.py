import logging
import time
import os
from threading import Thread
from flask import Flask
from binance_client import BinanceClient

# --- CONFIGURACIÓN DE RENDER (KEEP ALIVE) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot de Trading Operando 24/7"

def run_server():
    # Render asigna el puerto 10000 por defecto
    app.run(host='0.0.0.0', port=10000)

# --- CONFIGURACIÓN DEL BOT ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

client = BinanceClient()

def ejecutar_ciclo(objetivo_compra=95000):
    try:
        logging.info("Verificando mercado...")
        precio = client.get_price("BTCUSDT")
        saldo = client.get_balance()
        
        logging.info(f"Precio BTC: {precio} USDT | Saldo: {saldo} USDT")
        
        if precio <= objetivo_compra:
            logging.warning(f"¡Oportunidad! Precio {precio} <= {objetivo_compra}")
            cantidad = round(105 / precio, 4)
            orden = client.place_order("BTCUSDT", "BUY", cantidad)
            logging.info(f"Compra exitosa! ID: {orden['id']}")
        else:
            logging.info("Precio por encima del objetivo. Esperando...")
            
    except Exception as e:
        logging.error(f"Error en el ciclo: {e}")

if __name__ == "__main__":
    # 1. Iniciamos el servidor web en un hilo aparte para Render
    t = Thread(target=run_server)
    t.start()
    
    # 2. Bucle infinito del bot
    logging.info("Bot iniciado correctamente en la nube.")
    while True:
        ejecutar_ciclo()
        time.sleep(60) # Espera 60 segundos por ciclo
