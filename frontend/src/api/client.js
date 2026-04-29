const API_BASE = '/api'

export function getToken() {
  return localStorage.getItem('drinkme_token')
}

export function setToken(token) {
  localStorage.setItem('drinkme_token', token)
}

export function clearToken() {
  localStorage.removeItem('drinkme_token')
}

export async function apiRequest(path, options = {}) {
  const token = getToken()
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  }

  if (token) {
    headers.Authorization = `Token ${token}`
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers
  })

  if (response.status === 204) {
    return null
  }

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const message = data?.detail || data?.non_field_errors?.[0] || 'Запрос не выполнен'
    throw new Error(message)
  }

  return data
}

