import { apiRequest } from './client.js'

export function getCategories() {
  return apiRequest('/categories/')
}

export function getProducts(params = {}) {
  const search = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value) {
      search.set(key, value)
    }
  })
  const query = search.toString()
  return apiRequest(`/products/${query ? `?${query}` : ''}`)
}

