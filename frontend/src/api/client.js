const API_BASE = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '')

const fieldLabels = {
  username: 'Логин',
  email: 'Почта',
  password: 'Пароль',
  product_id: 'Товар',
  quantity: 'Количество',
  milk_type: 'Молоко',
  rating: 'Оценка',
  text: 'Текст'
}

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
    const fieldEntry = data && typeof data === 'object'
      ? Object.entries(data).find(([, value]) => Array.isArray(value) && value.length > 0)
      : null
    const fieldError = fieldEntry
      ? `${fieldLabels[fieldEntry[0]] || fieldEntry[0]}: ${fieldEntry[1][0]}`
      : null
    const message = data?.detail || data?.non_field_errors?.[0] || fieldError || 'Запрос не выполнен'
    throw new Error(message)
  }

  return data
}
