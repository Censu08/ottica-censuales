#!/bin/bash
set -e

echo "🚀 Inizializzazione Progetto Ottica Censuales"
echo "============================================="

# Verifica Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker non trovato. Installare Docker prima di continuare."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose non trovato. Installare Docker Compose prima di continuare."
    exit 1
fi

# Crea directory struttura progetto
echo "📁 Creazione struttura progetto..."
mkdir -p {backend,frontend,nginx,scripts,docs}

# Copia .env.example se non esiste
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📋 File .env creato da .env.example"
    echo "⚠️  IMPORTANTE: Modifica le variabili in .env prima di continuare"
fi

# Crea directory per i dati PostgreSQL
mkdir -p postgres_data

# Crea apps Django
echo "🐍 Creazione apps Django..."
mkdir -p backend/apps/{authentication,stores,products,inventory,orders,customers,analytics,integration,common}

# Crea file __init__.py per le apps
for app in authentication stores products inventory orders customers analytics integration common; do
    touch backend/apps/$app/__init__.py
    mkdir -p backend/apps/$app/migrations
    touch backend/apps/$app/migrations/__init__.py
done

# Build e avvio servizi
echo "🐳 Build delle immagini Docker..."
docker-compose build

echo "🗄️  Avvio database e Redis..."
docker-compose up -d db redis

echo "⏳ Attesa avvio database..."
sleep 10

echo "🔄 Esecuzione migrazioni Django..."
docker-compose run --rm backend python manage.py migrate

echo "👤 Creazione superuser Django..."
docker-compose run --rm backend python manage.py createsuperuser --noinput --username admin --email admin@otticacensuales.it || true

echo "📦 Installazione dipendenze frontend..."
docker-compose run --rm frontend npm install

echo "✅ Inizializzazione completata!"
echo ""
echo "🎯 Prossimi step:"
echo "1. Modifica le variabili in .env"
echo "2. docker-compose up per avviare tutto"
echo "3. Visita http://localhost:3000 per il frontend"
echo "4. Visita http://localhost:8000/admin per Django admin"
echo ""