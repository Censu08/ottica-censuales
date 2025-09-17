'use client'
import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchProducts } from '@/store/slices/productsSlice'
import Layout from '@/components/layout/Layout'
import ProductFilters from '@/components/products/ProductFilters'
import ProductGrid from '@/components/products/ProductGrid'

export default function ProductsPage() {
  const dispatch = useDispatch()
  const { products, productsLoading, filters, totalProducts } = useSelector(state => state.products)

  useEffect(() => {
    const searchParams = new URLSearchParams()
    
    if (filters.search) searchParams.append('search', filters.search)
    if (filters.category) searchParams.append('category__slug', filters.category)
    if (filters.brand) searchParams.append('brand__slug', filters.brand)
    
    dispatch(fetchProducts(Object.fromEntries(searchParams)))
  }, [dispatch, filters])

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">I Nostri Prodotti</h1>
          <p className="mt-2 text-gray-600">
            {totalProducts} prodotti disponibili
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1">
            <ProductFilters />
          </div>
          
          <div className="lg:col-span-3">
            <ProductGrid products={products} loading={productsLoading} />
          </div>
        </div>
      </div>
    </Layout>
  )
}