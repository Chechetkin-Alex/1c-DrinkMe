import { apiRequest } from './client.js'

export function getProductReviews(productId) {
  return apiRequest(`/products/${productId}/reviews/`)
}

export function createProductReview(productId, payload) {
  return apiRequest(`/products/${productId}/reviews/`, {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

