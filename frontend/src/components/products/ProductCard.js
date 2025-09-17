'use client'
import Image from 'next/image'
import Link from 'next/link'
import { useDispatch } from 'react-redux'
import { addItem } from '@/store/slices/cartSlice'
import { ShoppingCartIcon, EyeIcon } from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

export default function ProductCard({ product }) {
  const dispatch = useDispatch()

  const handleAddToCart = (e) => {
    e.preventDefault()
    e.stopPropagation()
    
    dispatch(addItem({
      product,
      quantity: 1
    }))
    
    toast.success(`${product.name} aggiunto al carrello`)
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('it-IT', {
      style: 'currency',
      currency: 'EUR'
    }).format(price)
  }

  return (
    <div className="group relative bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
      <Link href={`/prodotti/${product.slug}`}>
        <div className="aspect-square overflow-hidden rounded-t-lg bg-gray-100">
          {product.main_image ? (
            <Image
              src={product.main_image}
              alt={product.name}
              width={300}
              height={300}
              className="object-cover object-center group-hover:scale-105 transition-transform duration-200"
            />
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <EyeIcon className="h-16 w-16" />
            </div>
          )}
        </div>
        
        <div className="p-4">
          <div className="mb-2">
            <p className="text-sm text-gray-500">{product.brand?.name}</p>
            <h3 className="text-lg font-medium text-gray-900 group-hover:text-primary-600 transition-colors">
              {product.name}
            </h3>
          </div>
          
          {product.short_description && (
            <p className="text-sm text-gray-600 mb-3 line-clamp-2">
              {product.short_description}
            </p>
          )}
          
          <div className="flex items-center justify-between">
            <span className="text-xl font-semibold text-gray-900">
              {formatPrice(product.base_price)}
            </span>
            
            <button
              onClick={handleAddToCart}
              className="p-2 text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded-full transition-colors"
              title="Aggiungi al carrello"
            >
              <ShoppingCartIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
      </Link>
      
      {/* Badge per attributi speciali */}
      {product.is_prescription_required && (
        <div className="absolute top-2 left-2 bg-blue-600 text-white text-xs px-2 py-1 rounded">
          Su ricetta
        </div>
      )}
    </div>
  )
}