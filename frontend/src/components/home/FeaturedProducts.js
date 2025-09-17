'use client'
import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchProducts } from '@/store/slices/productsSlice'
import ProductGrid from '@/components/products/ProductGrid'
import Link from 'next/link'

export default function FeaturedProducts() {
  const dispatch = useDispatch()
  const { products, productsLoading } = useSelector(state => state.products)

  useEffect(() => {
    dispatch(fetchProducts({ page_size: 8 }))
  }, [dispatch])

  return (
    <div className="py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Prodotti in Evidenza</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Scopri la nostra selezione dei migliori prodotti per la tua vista
          </p>
        </div>

        <ProductGrid products={products.slice(0, 8)} loading={productsLoading} />

        <div className="text-center mt-12">
          <Link href="/prodotti" className="btn-primary">
            Vedi tutti i prodotti
          </Link>
        </div>
      </div>
    </div>
  )
}