import { apiRequest, clearToken, setToken } from './client.js'

export async function login(payload) {
  const data = await apiRequest('/auth/login/', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
  setToken(data.token)
  return data.user
}

export async function register(payload) {
  const data = await apiRequest('/auth/register/', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
  setToken(data.token)
  return data.user
}

export async function logout() {
  try {
    await apiRequest('/auth/logout/', { method: 'POST' })
  } finally {
    clearToken()
  }
}

export function getMe() {
  return apiRequest('/auth/me/')
}

