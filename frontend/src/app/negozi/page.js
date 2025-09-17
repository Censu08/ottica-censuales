'use client'
import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import {
  PhoneIcon,
  MapPinIcon,
  ClockIcon,
  UserIcon
} from '@heroicons/react/24/outline'

// Importiamo la mappa dinamicamente per evitare problemi SSR
const StoreMap = dynamic(() => import('@/components/stores/StoreMap'), {
  ssr: false,
  loading: () => <div className="h-96 bg-gray-200 animate-pulse rounded-lg flex items-center justify-center">
    <p className="text-gray-500">Caricamento mappa...</p>
  </div>
})

export default function StoresPage() {
  const [stores, setStores] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedStore, setSelectedStore] = useState(null)
  const [mapConfig, setMapConfig] = useState(null)

  useEffect(() => {
    fetchStores()
  }, [])

  const fetchStores = async () => {
    try {
      setLoading(true)

      // Fetch dati per la mappa
      const mapResponse = await fetch('/api/stores/map-data/')
      const mapData = await mapResponse.json()

      // Fetch lista completa negozi
      const storesResponse = await fetch('/api/stores/')
      const storesData = await storesResponse.json()

      setStores(storesData.results || storesData)
      setMapConfig(mapData.map_config)

    } catch (error) {
      console.error('Errore nel caricamento dei negozi:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStoreSelect = (store) => {
    setSelectedStore(store)
    // Scroll alla card del negozio selezionato
    const element = document.getElementById(`store-${store.id}`)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
        <p className="mt-4 text-gray-600">Caricamento negozi...</p>
      </div>
    </div>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">I Nostri Negozi</h1>
            <p className="mt-4 text-lg text-gray-600">
              Trova il negozio Ottica Censuales più vicino a te a Palermo
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Mappa */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Localizza i Negozi sulla Mappa
          </h2>
          <div className="h-96 rounded-lg overflow-hidden border">
            <StoreMap
              stores={stores}
              config={mapConfig}
              onStoreSelect={handleStoreSelect}
              selectedStore={selectedStore}
            />
          </div>
        </div>

        {/* Griglia Negozi */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">
            Elenco Negozi ({stores.length})
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {stores.map((store) => (
              <StoreCard
                key={store.id}
                store={store}
                isSelected={selectedStore?.id === store.id}
                onClick={() => handleStoreSelect(store)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// Componente Card del singolo negozio
function StoreCard({ store, isSelected, onClick }) {
  return (
    <div
      id={`store-${store.id}`}
      className={`border rounded-lg p-6 hover:shadow-lg transition-all cursor-pointer ${
        isSelected ? 'border-primary-500 ring-2 ring-primary-200 bg-primary-50' : 'border-gray-200 hover:border-gray-300'
      }`}
      onClick={onClick}
    >
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          {store.name}
        </h3>
        {store.description && (
          <p className="text-sm text-gray-600">{store.description}</p>
        )}
      </div>

      <div className="space-y-3">
        {/* Indirizzo */}
        <div className="flex items-start space-x-3">
          <MapPinIcon className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-sm font-medium text-gray-900">Indirizzo</p>
            <p className="text-sm text-gray-600">{store.formatted_address || store.address}</p>
          </div>
        </div>

        {/* Telefono */}
        {store.phone && (
          <div className="flex items-center space-x-3">
            <PhoneIcon className="h-5 w-5 text-gray-400 flex-shrink-0" />
            <div>
              <p className="text-sm font-medium text-gray-900">Telefono</p>
              <a
                href={`tel:${store.phone}`}
                className="text-sm text-primary-600 hover:text-primary-800"
              >
                {store.phone}
              </a>
            </div>
          </div>
        )}

        {/* Ottico di riferimento */}
        {store.optician_name && (
          <div className="flex items-center space-x-3">
            <UserIcon className="h-5 w-5 text-gray-400 flex-shrink-0" />
            <div>
              <p className="text-sm font-medium text-gray-900">Ottico di Riferimento</p>
              <p className="text-sm text-gray-600">{store.optician_name}</p>
            </div>
          </div>
        )}

        {/* Orari */}
        {store.formatted_opening_hours && (
          <div className="flex items-start space-x-3">
            <ClockIcon className="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-sm font-medium text-gray-900">Orari di Apertura</p>
              <div className="text-sm text-gray-600 whitespace-pre-line">
                {store.formatted_opening_hours}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Azioni */}
      <div className="mt-4 pt-4 border-t border-gray-200 flex space-x-2">
        <button
          onClick={(e) => {
            e.stopPropagation()
            // Apri navigatore con le coordinate
            window.open(`https://www.google.com/maps/dir/?api=1&destination=${store.latitude},${store.longitude}`)
          }}
          className="flex-1 bg-primary-600 text-white px-3 py-2 rounded text-sm font-medium hover:bg-primary-700 transition-colors"
        >
          Indicazioni
        </button>

        {store.phone && (
          <button
            onClick={(e) => {
              e.stopPropagation()
              window.open(`tel:${store.phone}`)
            }}
            className="flex-1 border border-gray-300 text-gray-700 px-3 py-2 rounded text-sm font-medium hover:bg-gray-50 transition-colors"
          >
            Chiama
          </button>
        )}
      </div>
    </div>
  )
}