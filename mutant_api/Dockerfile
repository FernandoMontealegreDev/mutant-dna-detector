# Usar la imagen oficial de Python 3.12.5 como base
FROM python:3.12.5-slim

# Instalar dependencias del sistema necesarias para compilación (ejemplo: para psycopg2 o cualquier librería C)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requisitos al contenedor
COPY requirements.txt /app/

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto al contenedor
COPY . /app/

# Ejecutar las migraciones de Alembic (asegúrate de que Alembic esté configurado correctamente)
RUN alembic upgrade head

# Exponer el puerto en el que se ejecutará la aplicación (FastAPI por defecto usa el puerto 8000)
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn en producción
# Usamos "uvicorn" para iniciar FastAPI, con "host=0.0.0.0" para que sea accesible desde fuera del contenedor.
# En producción no usamos "--reload" para mejor rendimiento
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]