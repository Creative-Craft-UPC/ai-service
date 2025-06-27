# Usa una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requerimientos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente de la aplicación
COPY . .

# Exponer el puerto (ajustado a 8003 para este servicio)
EXPOSE 8003

# Comando para ejecutar el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
