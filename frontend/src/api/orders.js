import { apiRequest } from './client.js'

export function getOrders() {
  return apiRequest('/orders/')
}

export function createOrder() {
  return apiRequest('/orders/', {
    method: 'POST'
  })
}

export function updateOrder(id, payload) {
  return apiRequest(`/orders/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(payload)
  })
}
