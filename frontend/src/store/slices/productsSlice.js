import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '@/lib/api'

// Async thunks
export const fetchProducts = createAsyncThunk(
  'products/fetchProducts',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await api.get('/products/', { params })
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Errore nel caricamento prodotti')
    }
  }
)

export const fetchProductDetail = createAsyncThunk(
  'products/fetchProductDetail',
  async (slug, { rejectWithValue }) => {
    try {
      const response = await api.get(`/products/${slug}/`)
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Errore nel caricamento prodotto')
    }
  }
)

export const fetchCategories = createAsyncThunk(
  'products/fetchCategories',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/products/categories/')
      return response.data
    } catch (error) {
      return rejectWithValue('Errore nel caricamento categorie')
    }
  }
)

export const fetchBrands = createAsyncThunk(
  'products/fetchBrands',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/products/brands/')
      return response.data
    } catch (error) {
      return rejectWithValue('Errore nel caricamento marchi')
    }
  }
)

const productsSlice = createSlice({
  name: 'products',
  initialState: {
    // Lista prodotti
    products: [],
    productsLoading: false,
    productsError: null,
    totalProducts: 0,
    currentPage: 1,
    
    // Dettaglio prodotto
    currentProduct: null,
    productLoading: false,
    productError: null,
    
    // Categorie e brands
    categories: [],
    brands: [],
    categoriesLoading: false,
    brandsLoading: false,
    
    // Filtri
    filters: {
      category: '',
      brand: '',
      priceRange: [0, 1000],
      search: '',
    },
  },
  reducers: {
    updateFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload }
    },
    clearFilters: (state) => {
      state.filters = {
        category: '',
        brand: '',
        priceRange: [0, 1000],
        search: '',
      }
    },
    clearCurrentProduct: (state) => {
      state.currentProduct = null
      state.productError = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch products
      .addCase(fetchProducts.pending, (state) => {
        state.productsLoading = true
        state.productsError = null
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.productsLoading = false
        state.products = action.payload.results || action.payload
        state.totalProducts = action.payload.count || action.payload.length
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.productsLoading = false
        state.productsError = action.payload
      })
      // Fetch product detail
      .addCase(fetchProductDetail.pending, (state) => {
        state.productLoading = true
        state.productError = null
      })
      .addCase(fetchProductDetail.fulfilled, (state, action) => {
        state.productLoading = false
        state.currentProduct = action.payload
      })
      .addCase(fetchProductDetail.rejected, (state, action) => {
        state.productLoading = false
        state.productError = action.payload
      })
      // Fetch categories
      .addCase(fetchCategories.pending, (state) => {
        state.categoriesLoading = true
      })
      .addCase(fetchCategories.fulfilled, (state, action) => {
        state.categoriesLoading = false
        state.categories = action.payload.results || action.payload
      })
      // Fetch brands
      .addCase(fetchBrands.pending, (state) => {
        state.brandsLoading = true
      })
      .addCase(fetchBrands.fulfilled, (state, action) => {
        state.brandsLoading = false
        state.brands = action.payload.results || action.payload
      })
  },
})

export const { updateFilters, clearFilters, clearCurrentProduct } = productsSlice.actions
export default productsSlice.reducer