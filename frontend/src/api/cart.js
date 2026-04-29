import { apiRequest } from './client.js'

export function getCart() {
  return apiRequest('/cart/')
}

export function addCartItem(payload) {
  return apiRequest('/cart/items/', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function updateCartItem(id, payload) {
  return apiRequest(`/cart/items/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}

export function deleteCartItem(id) {
  return apiRequest(`/cart/items/${id}/`, {
    method: 'DELETE'
  })
}

