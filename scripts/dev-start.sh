#!/bin/bash
set -e

echo "🚀 Avvio ambiente sviluppo Ottica Censuales"
echo "==========================================="

# Verifica se .env esiste
if [ ! -f .env ]; then
    echo "❌ File .env non trovato. Esegui prima ./scripts/init-project.sh"
    exit 1
fi

# Avvia tutti i servizi
echo "🐳 Avvio servizi Docker..."
docker-compose up -d

echo "⏳ Attendere l'avvio completo dei servizi..."
sleep 15

# Controlla lo stato dei servizi
echo "📊 Stato servizi:"
docker-compose ps

echo ""
echo "✅ Ambiente di sviluppo avviato!"
echo ""
echo "🌐 Servizi disponibili:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- Django Admin: http://localhost:8000/admin"
echo "- Database: localhost:5432"
echo "- Redis: localhost:6379"
echo ""
echo "📝 Log servizi:"
echo "docker-compose logs -f [service-name]"
echo ""