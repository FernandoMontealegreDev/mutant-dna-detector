# Usar la imagen oficial de Python 3.12.5 como base
FROM python:3.12.5-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requisitos y el código fuente al contenedor
COPY requirements.txt /app/

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto al contenedor
COPY . /app/

# Ejecutar las migraciones de alembic
RUN alembic upgrade head

# Exponer el puerto en el que se ejecutará la aplicación (por defecto FastAPI usa el puerto 8000)
EXPOSE 8000

# Comando para ejecutar la aplicación al iniciar el contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]