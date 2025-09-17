'use client'
import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix per le icone di default di Leaflet in Next.js
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: '/images/marker-icon-2x.png',
  iconUrl: '/images/marker-icon.png',
  shadowUrl: '/images/marker-shadow.png',
})

export default function StoreMap({ stores = [], config, onStoreSelect, selectedStore }) {
  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)
  const markersRef = useRef(new Map())

  useEffect(() => {
    if (!mapRef.current || mapInstanceRef.current) return

    // Configurazione mappa centrata su Palermo
    const mapConfig = config || {
      center: { lat: 38.1157, lng: 13.3613 },
      zoom: 12
    }

    // Inizializza la mappa
    const map = L.map(mapRef.current).setView(
      [mapConfig.center.lat, mapConfig.center.lng],
      mapConfig.zoom
    )

    // Aggiungi tiles di OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map)

    mapInstanceRef.current = map

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [config])

  // Aggiorna i marker quando cambiano i negozi
  useEffect(() => {
    if (!mapInstanceRef.current || !stores.length) return

    // Rimuovi marker esistenti
    markersRef.current.forEach(marker => {
      mapInstanceRef.current.removeLayer(marker)
    })
    markersRef.current.clear()

    // Crea icona personalizzata per i negozi
    const storeIcon = L.divIcon({
      html: `
        <div class="store-marker">
          <div class="marker-pin"></div>
          <div class="marker-pulse"></div>
        </div>
      `,
      className: 'custom-marker',
      iconSize: [30, 30],
      iconAnchor: [15, 30]
    })

    const selectedIcon = L.divIcon({
      html: `
        <div class="store-marker selected">
          <div class="marker-pin selected"></div>
          <div class="marker-pulse selected"></div>
        </div>
      `,
      className: 'custom-marker',
      iconSize: [35, 35],
      iconAnchor: [17.5, 35]
    })

    // Aggiungi marker per ogni negozio
    stores.forEach(store => {
      if (!store.latitude || !store.longitude) return

      const isSelected = selectedStore?.id === store.id
      const marker = L.marker(
        [parseFloat(store.latitude), parseFloat(store.longitude)],
        { icon: isSelected ? selectedIcon : storeIcon }
      )

      // Popup con informazioni del negozio
      const popupContent = `
        <div class="store-popup">
          <h3 class="font-semibold text-gray-900 mb-2">${store.name}</h3>
          <p class="text-sm text-gray-600 mb-2">${store.address}</p>
          ${store.optician_name ? `<p class="text-sm"><strong>Ottico:</strong> ${store.optician_name}</p>` : ''}
          ${store.phone ? `<p class="text-sm"><strong>Tel:</strong> <a href="tel:${store.phone}" class="text-primary-600">${store.phone}</a></p>` : ''}
          <div class="mt-3 flex space-x-2">
            <a href="https://www.google.com/maps/dir/?api=1&destination=${store.latitude},${store.longitude}"
               target="_blank"
               class="bg-primary-600 text-white px-3 py-1 rounded text-sm hover:bg-primary-700">
              Indicazioni
            </a>
            ${store.phone ? `<a href="tel:${store.phone}" class="border border-gray-300 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-50">Chiama</a>` : ''}
          </div>
        </div>
      `

      marker.bindPopup(popupContent)

      // Event listener per la selezione del negozio
      marker.on('click', () => {
        if (onStoreSelect) {
          onStoreSelect(store)
        }
      })

      // Aggiungi marker alla mappa
      marker.addTo(mapInstanceRef.current)
      markersRef.current.set(store.id, marker)
    })

    // Adatta la vista per mostrare tutti i marker
    if (stores.length > 0) {
      const group = new L.featureGroup(Array.from(markersRef.current.values()))
      mapInstanceRef.current.fitBounds(group.getBounds().pad(0.1))
    }

  }, [stores, selectedStore, onStoreSelect])

  // Effetto per centrare sulla selezione
  useEffect(() => {
    if (selectedStore && mapInstanceRef.current) {
      const marker = markersRef.current.get(selectedStore.id)
      if (marker) {
        // Aggiorna l'icona del marker selezionato
        markersRef.current.forEach((m, id) => {
          const isSelected = id === selectedStore.id
          const icon = isSelected ?
            L.divIcon({
              html: `
                <div class="store-marker selected">
                  <div class="marker-pin selected"></div>
                  <div class="marker-pulse selected"></div>
                </div>
              `,
              className: 'custom-marker',
              iconSize: [35, 35],
              iconAnchor: [17.5, 35]
            }) :
            L.divIcon({
              html: `
                <div class="store-marker">
                  <div class="marker-pin"></div>
                  <div class="marker-pulse"></div>
                </div>
              `,
              className: 'custom-marker',
              iconSize: [30, 30],
              iconAnchor: [15, 30]
            })

          m.setIcon(icon)
        })

        // Centra la mappa sul marker selezionato
        mapInstanceRef.current.setView(
          [selectedStore.latitude, selectedStore.longitude],
          15,
          { animate: true }
        )

        // Apri il popup
        marker.openPopup()
      }
    }
  }, [selectedStore])

  return (
    <>
      <div ref={mapRef} className="w-full h-full" />

      {/* Stili CSS inline per i marker personalizzati */}
      <style jsx global>{`
        .store-marker {
          position: relative;
        }

        .marker-pin {
          width: 20px;
          height: 20px;
          background: #dc2626;
          border: 2px solid white;
          border-radius: 50% 50% 50% 0;
          position: absolute;
          transform: rotate(-45deg);
          left: 50%;
          top: 50%;
          margin: -10px 0 0 -10px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }

        .marker-pin.selected {
          background: #2563eb;
          width: 24px;
          height: 24px;
          margin: -12px 0 0 -12px;
        }

        .marker-pin::after {
          content: '';
          width: 8px;
          height: 8px;
          margin: 6px 0 0 6px;
          background: white;
          position: absolute;
          border-radius: 50%;
        }

        .marker-pin.selected::after {
          width: 10px;
          height: 10px;
          margin: 7px 0 0 7px;
        }

        .marker-pulse {
          background: rgba(220, 38, 38, 0.2);
          border-radius: 50%;
          height: 14px;
          width: 14px;
          position: absolute;
          left: 50%;
          top: 50%;
          margin: -7px 0 0 -7px;
          transform: rotateX(55deg);
          z-index: -2;
          animation: pulsate 1s ease-out infinite;
        }

        .marker-pulse.selected {
          background: rgba(37, 99, 235, 0.2);
          height: 18px;
          width: 18px;
          margin: -9px 0 0 -9px;
        }

        @keyframes pulsate {
          0% {
            transform: rotateX(55deg) scale(0.6);
            opacity: 1;
          }
          100% {
            transform: rotateX(55deg) scale(1);
            opacity: 0;
          }
        }

        .store-popup h3 {
          margin: 0 0 8px 0;
          font-size: 16px;
          font-weight: 600;
        }

        .store-popup p {
          margin: 4px 0;
          font-size: 14px;
        }

        .store-popup a {
          text-decoration: none;
        }

        .store-popup a:hover {
          text-decoration: underline;
        }
      `}</style>
    </>
  )
}