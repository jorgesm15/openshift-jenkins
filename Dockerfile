# Usamos la imagen base de Node.js (en este caso, versión 18 y la variante de Alpine)
FROM node:18-alpine

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo package.json y package-lock.json para instalar dependencias primero
COPY package*.json ./

# Instalamos las dependencias de la aplicación
RUN npm install

# Copiamos el resto de los archivos del proyecto en el contenedor
COPY . .

# Exponemos el puerto donde la aplicación se ejecutará (suponiendo que es el puerto 3000)
EXPOSE 3000

# Comando para arrancar la aplicación
CMD ["npm", "start"]
