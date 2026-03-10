# 1. Elegimos una imagen base de Python (la versión 'slim' es ligera y eficiente)
FROM python:3.11-slim

# 2. Definimos el directorio dentro del contenedor donde vivirá tu bot
WORKDIR /app

# 3. Copiamos solo el archivo de requerimientos primero (esto hace que sea más rápido reconstruir)
COPY requirements.txt .

# 4. Instalamos las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto de tu código fuente al contenedor
COPY . .

# 6. Definimos la variable de entorno para que Python no guarde archivos .pyc (limpieza)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 7. Comando para ejecutar tu bot
CMD ["python", "bot.py"]