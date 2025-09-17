import { createSlice } from '@reduxjs/toolkit'

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [],
    total: 0,
    itemsCount: 0,
  },
  reducers: {
    addItem: (state, action) => {
      const { product, variant, quantity = 1 } = action.payload
      const existingItem = state.items.find(
        item => item.product.id === product.id && 
        (item.variant?.id || null) === (variant?.id || null)
      )

      if (existingItem) {
        existingItem.quantity += quantity
      } else {
        state.items.push({
          product,
          variant,
          quantity,
          price: variant?.price || product.base_price,
        })
      }

      // Ricalcola totali
      state.itemsCount = state.items.reduce((count, item) => count + item.quantity, 0)
      state.total = state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
    },

    removeItem: (state, action) => {
      const { productId, variantId } = action.payload
      state.items = state.items.filter(
        item => !(item.product.id === productId && (item.variant?.id || null) === (variantId || null))
      )

      // Ricalcola totali
      state.itemsCount = state.items.reduce((count, item) => count + item.quantity, 0)
      state.total = state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
    },

    updateQuantity: (state, action) => {
      const { productId, variantId, quantity } = action.payload
      const item = state.items.find(
        item => item.product.id === productId && (item.variant?.id || null) === (variantId || null)
      )

      if (item) {
        item.quantity = quantity
      }

      // Ricalcola totali
      state.itemsCount = state.items.reduce((count, item) => count + item.quantity, 0)
      state.total = state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
    },

    clearCart: (state) => {
      state.items = []
      state.total = 0
      state.itemsCount = 0
    },
  },
})

export const { addItem, removeItem, updateQuantity, clearCart } = cartSlice.actions
export default cartSlice.reducer