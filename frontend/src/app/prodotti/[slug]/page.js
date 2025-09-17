'use client'
import { useEffect } from 'react'
import { useParams } from 'next/navigation'
import { useDispatch, useSelector } from 'react-redux'
import { fetchProductDetail, clearCurrentProduct } from '@/store/slices/productsSlice'
import { addItem } from '@/store/slices/cartSlice'
import Layout from '@/components/layout/Layout'
import Image from 'next/image'
import { useState } from 'react'
import toast from 'react-hot-toast'
import { ShoppingCartIcon, HeartIcon } from '@heroicons/react/24/outline'

export default function ProductDetailPage() {
  const params = useParams()
  const dispatch = useDispatch()
  const { currentProduct: product, productLoading, productError } = useSelector(state => state.products)
  const [selectedVariant, setSelectedVariant] = useState(null)
  const [quantity, setQuantity] = useState(1)

  useEffect(() => {
    if (params.slug) {
      dispatch(fetchProductDetail(params.slug))
    }
    
    return () => {
      dispatch(clearCurrentProduct())
    }
  }, [dispatch, params.slug])

  const handleAddToCart = () => {
    if (!product) return
    
    dispatch(addItem({
      product,
      variant: selectedVariant,
      quantity
    }))
    
    toast.success(`${product.name} aggiunto al carrello`)
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('it-IT', {
      style: 'currency',
      currency: 'EUR'
    }).format(price)
  }

  if (productLoading) {
    return (
      <Layout>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="aspect-square bg-gray-300 rounded-lg" />
              <div className="space-y-4">
                <div className="h-8 bg-gray-300 rounded w-3/4" />
                <div className="h-4 bg-gray-300 rounded w-1/2" />
                <div className="h-6 bg-gray-300 rounded w-1/4" />
                <div className="h-20 bg-gray-300 rounded" />
              </div>
            </div>
          </div>
        </div>
      </Layout>
    )
  }

  if (productError || !product) {
    return (
      <Layout>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Prodotto non trovato</h1>
            <p className="text-gray-600">Il prodotto che stai cercando non esiste o non è più disponibile.</p>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {/* Immagini prodotto */}
          <div>
            <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden mb-4">
              {product.main_image ? (
                <Image
                  src={product.main_image}
                  alt={product.name}
                  width={600}
                  height={600}
                  className="object-cover object-center w-full h-full"
                />
              ) : (
                <div className="flex items-center justify-center h-full text-gray-400">
                  <ShoppingCartIcon className="h-24 w-24" />
                </div>
              )}
            </div>
            
            {/* Galleria immagini */}
            {product.images && product.images.length > 0 && (
              <div className="grid grid-cols-4 gap-4">
                {product.images.slice(0, 4).map((image, index) => (
                  <div key={index} className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                    <Image
                      src={image.image}
                      alt={image.alt_text || product.name}
                      width={150}
                      height={150}
                      className="object-cover object-center w-full h-full"
                    />
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Informazioni prodotto */}
          <div>
            <div className="mb-4">
              <p className="text-sm text-gray-500">{product.brand?.name}</p>
              <h1 className="text-3xl font-bold text-gray-900">{product.name}</h1>
              <p className="text-xl text-gray-600 mt-2">{product.short_description}</p>
            </div>

            <div className="mb-6">
              <p className="text-3xl font-bold text-gray-900">
                {formatPrice(selectedVariant?.price_adjustment ? 
                  parseFloat(product.base_price) + parseFloat(selectedVariant.price_adjustment) : 
                  product.base_price)}
              </p>
            </div>

            {/* Varianti */}
            {product.variants && product.variants.length > 0 && (
              <div className="mb-6">
                <h3 className="text-lg font-medium text-gray-900 mb-3">Opzioni disponibili</h3>
                <div className="grid grid-cols-2 gap-3">
                  {product.variants.map((variant) => (
                    <button
                      key={variant.id}
                      onClick={() => setSelectedVariant(variant)}
                      className={`p-3 border rounded-lg text-left transition-colors ${
                        selectedVariant?.id === variant.id
                          ? 'border-primary-600 bg-primary-50 text-primary-600'
                          : 'border-gray-300 hover:border-gray-400'
                      }`}
                    >
                      <div className="font-medium">{variant.name}</div>
                      {variant.price_adjustment !== 0 && (
                        <div className="text-sm text-gray-600">
                          {variant.price_adjustment > 0 ? '+' : ''}{formatPrice(variant.price_adjustment)}
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Quantità */}
            <div className="mb-6">
              <label htmlFor="quantity" className="block text-lg font-medium text-gray-900 mb-2">
                Quantità
              </label>
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="w-10 h-10 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                >
                  -
                </button>
                <span className="text-xl font-medium w-12 text-center">{quantity}</span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="w-10 h-10 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                >
                  +
                </button>
              </div>
            </div>

            {/* Pulsanti azione */}
            <div className="space-y-4">
              <button
                onClick={handleAddToCart}
                className="w-full btn-primary flex items-center justify-center space-x-2"
              >
                <ShoppingCartIcon className="h-5 w-5" />
                <span>Aggiungi al carrello</span>
              </button>
              
              <button className="w-full btn-secondary flex items-center justify-center space-x-2">
                <HeartIcon className="h-5 w-5" />
                <span>Aggiungi ai preferiti</span>
              </button>
            </div>

            {/* Attributi ottici */}
            {product.optical_attributes && Object.keys(product.optical_attributes).length > 0 && (
              <div className="mt-8">
                <h3 className="text-lg font-medium text-gray-900 mb-3">Caratteristiche</h3>
                <div className="space-y-2">
                  {Object.entries(product.optical_attributes).map(([key, value]) => (
                    <div key={key} className="flex justify-between py-2 border-b border-gray-200">
                      <span className="text-gray-600 capitalize">{key.replace('_', ' ')}</span>
                      <span className="font-medium">{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Descrizione completa */}
        {product.description && (
          <div className="border-t border-gray-200 pt-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Descrizione</h2>
            <div className="prose max-w-none text-gray-600">
              {product.description}
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
}