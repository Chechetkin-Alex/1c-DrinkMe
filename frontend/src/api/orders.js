import { apiRequest } from './client.js'

export function getOrders() {
  return apiRequest('/orders/')
}

export function createOrder() {
  return apiRequest('/orders/', {
    method: 'POST'
  })
}

