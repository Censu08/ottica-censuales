FROM node:18-alpine

WORKDIR /app

# Install dependencies (tutte, non solo production)
COPY package*.json ./
RUN npm install

# Copia solo i file di configurazione inizialmente
COPY next.config.js ./
COPY tsconfig.json ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

# Il resto del codice sarà montato via volume

# Expose port
EXPOSE 3000

# Start in development mode con hot reload
CMD ["npm", "run", "dev"]