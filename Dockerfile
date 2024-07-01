# Utiliza la imagen oficial de Rasa como base
FROM rasa/rasa:3.0.0

# Copia todo el contenido del directorio actual al contenedor
COPY . /app

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Expone el puerto 5005 para el servidor de Rasa
EXPOSE 5005

# Comando para ejecutar el servidor de Rasa con las acciones personalizadas
CMD ["rasa", "run", "-m", "models", "--enable-api", "--cors", "*", "--debug"]