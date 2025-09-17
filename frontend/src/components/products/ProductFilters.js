'use client'
import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { updateFilters, clearFilters, fetchCategories, fetchBrands } from '@/store/slices/productsSlice'
import { FunnelIcon, XMarkIcon } from '@heroicons/react/24/outline'

export default function ProductFilters() {
  const dispatch = useDispatch()
  const { categories, brands, filters, categoriesLoading, brandsLoading } = useSelector(state => state.products)
  const [showFilters, setShowFilters] = useState(false)

  useEffect(() => {
    dispatch(fetchCategories())
    dispatch(fetchBrands())
  }, [dispatch])

  const handleFilterChange = (filterType, value) => {
    dispatch(updateFilters({ [filterType]: value }))
  }

  const handleClearFilters = () => {
    dispatch(clearFilters())
  }

  const hasActiveFilters = Object.values(filters).some(filter => 
    filter !== '' && !(Array.isArray(filter) && filter.every(val => val === 0 || val === 1000))
  )

  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      {/* Mobile filter toggle */}
      <div className="flex items-center justify-between md:hidden mb-4">
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center space-x-2 text-gray-700"
        >
          <FunnelIcon className="h-5 w-5" />
          <span>Filtri</span>
        </button>
        
        {hasActiveFilters && (
          <button
            onClick={handleClearFilters}
            className="flex items-center space-x-1 text-red-600 text-sm"
          >
            <XMarkIcon className="h-4 w-4" />
            <span>Cancella</span>
          </button>
        )}
      </div>

      {/* Filters content */}
      <div className={`space-y-6 ${showFilters ? 'block' : 'hidden md:block'}`}>
        {/* Search */}
        <div>
          <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
            Cerca prodotti
          </label>
          <input
            type="text"
            id="search"
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            placeholder="Nome, modello, SKU..."
            className="input-field"
          />
        </div>

        {/* Categories */}
        <div>
          <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
            Categoria
          </label>
          <select
            id="category"
            value={filters.category}
            onChange={(e) => handleFilterChange('category', e.target.value)}
            className="input-field"
            disabled={categoriesLoading}
          >
            <option value="">Tutte le categorie</option>
            {categories.map((category) => (
              <option key={category.id} value={category.slug}>
                {category.name}
              </option>
            ))}
          </select>
        </div>

        {/* Brands */}
        <div>
          <label htmlFor="brand" className="block text-sm font-medium text-gray-700 mb-2">
            Marchio
          </label>
          <select
            id="brand"
            value={filters.brand}
            onChange={(e) => handleFilterChange('brand', e.target.value)}
            className="input-field"
            disabled={brandsLoading}
          >
            <option value="">Tutti i marchi</option>
            {brands.map((brand) => (
              <option key={brand.id} value={brand.slug}>
                {brand.name}
              </option>
            ))}
          </select>
        </div>

        {/* Price Range */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Fascia di prezzo: €{filters.priceRange[0]} - €{filters.priceRange[1]}
          </label>
          <div className="flex space-x-4">
            <input
              type="number"
              placeholder="Min"
              value={filters.priceRange[0]}
              onChange={(e) => handleFilterChange('priceRange', [parseInt(e.target.value) || 0, filters.priceRange[1]])}
              className="input-field flex-1"
            />
            <input
              type="number"
              placeholder="Max"
              value={filters.priceRange[1]}
              onChange={(e) => handleFilterChange('priceRange', [filters.priceRange[0], parseInt(e.target.value) || 1000])}
              className="input-field flex-1"
            />
          </div>
        </div>

        {/* Clear filters button (desktop) */}
        {hasActiveFilters && (
          <div className="hidden md:block">
            <button
              onClick={handleClearFilters}
              className="w-full btn-secondary"
            >
              Cancella filtri
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
