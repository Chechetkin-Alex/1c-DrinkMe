import { useEffect, useMemo, useState } from 'react'
import { Link, NavLink, Route, Routes, useNavigate } from 'react-router-dom'

import { getMe, login, logout, register } from './api/auth.js'
import { addCartItem, deleteCartItem, getCart } from './api/cart.js'
import { getCategories, getProducts } from './api/catalog.js'
import { createOrder, getOrders } from './api/orders.js'
import { getToken } from './api/client.js'

const milkOptions = [
  ['regular', 'обычное'],
  ['alternative', 'альтернативное'],
  ['oat', 'овсяное'],
  ['coconut', 'кокосовое'],
  ['banana', 'банановое'],
  ['almond', 'миндальное'],
  ['none', 'без молока']
]

export function App() {
  const [user, setUser] = useState(null)
  const [authChecked, setAuthChecked] = useState(false)

  useEffect(() => {
    if (!getToken()) {
      setAuthChecked(true)
      return
    }

    getMe()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setAuthChecked(true))
  }, [])

  async function handleLogout() {
    await logout()
    setUser(null)
  }

  if (!authChecked) {
    return <div className="page">Загрузка</div>
  }

  return (
    <div className="app">
      <header className="topbar">
        <Link className="brand" to="/">DrinkMe</Link>
        <nav>
          <NavLink to="/">Каталог</NavLink>
          <NavLink to="/cart">Корзина</NavLink>
          <NavLink to="/orders">Заказы</NavLink>
        </nav>
        <div className="user-box">
          {user ? (
            <>
              <span>{user.username}</span>
              {user.is_phystech_student && <span className="badge">МФТИ</span>}
              <button onClick={handleLogout}>Выйти</button>
            </>
          ) : (
            <NavLink to="/login">Войти</NavLink>
          )}
        </div>
      </header>

      <main className="page">
        <Routes>
          <Route path="/" element={<CatalogPage user={user} />} />
          <Route path="/cart" element={<CartPage user={user} />} />
          <Route path="/orders" element={<OrdersPage user={user} />} />
          <Route path="/login" element={<AuthPage onAuth={setUser} />} />
        </Routes>
      </main>
    </div>
  )
}

function CatalogPage({ user }) {
  const [categories, setCategories] = useState([])
  const [products, setProducts] = useState([])
  const [category, setCategory] = useState('')
  const [search, setSearch] = useState('')
  const [milkType, setMilkType] = useState('regular')
  const [message, setMessage] = useState('')

  useEffect(() => {
    getCategories().then(setCategories)
  }, [])

  useEffect(() => {
    getProducts({ category, search }).then(setProducts)
  }, [category, search])

  async function addToCart(product) {
    if (!user) {
      setMessage('Сначала войдите в аккаунт')
      return
    }

    await addCartItem({
      product_id: product.id,
      quantity: 1,
      milk_type: product.product_type === 'drink' ? milkType : 'none'
    })
    setMessage(`${product.name} добавлен в корзину`)
  }

  return (
    <section>
      <div className="section-head">
        <div>
          <h1>Каталог</h1>
          <p>Кофе, выпечка и товары для дома рядом с МФТИ</p>
        </div>
      </div>

      <div className="toolbar">
        <input
          placeholder="Поиск"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <select value={category} onChange={(event) => setCategory(event.target.value)}>
          <option value="">Все категории</option>
          {categories.map((item) => (
            <option key={item.id} value={item.slug}>{item.name}</option>
          ))}
        </select>
        <select value={milkType} onChange={(event) => setMilkType(event.target.value)}>
          {milkOptions.map(([value, label]) => (
            <option key={value} value={value}>{label}</option>
          ))}
        </select>
      </div>

      {message && <div className="notice">{message}</div>}

      <div className="product-grid">
        {products.map((product) => (
          <article className="product-card" key={product.id}>
            <div className="product-type">{product.category.name}</div>
            <h2>{product.name}</h2>
            <p>{product.description || 'Описание появится позже'}</p>
            <div className="card-bottom">
              <strong>{product.price} ₽</strong>
              <button onClick={() => addToCart(product)}>В корзину</button>
            </div>
            {product.is_student_special && <span className="special">студенческое комбо</span>}
          </article>
        ))}
      </div>
    </section>
  )
}

function CartPage({ user }) {
  const [cart, setCart] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (user) {
      getCart().then(setCart)
    }
  }, [user])

  async function removeItem(id) {
    await deleteCartItem(id)
    setCart(await getCart())
  }

  async function checkout() {
    const order = await createOrder()
    setCart(await getCart())
    setMessage(`Заказ №${order.id} создан`)
  }

  if (!user) {
    return <EmptyState title="Нужен вход" text="Корзина доступна после входа" />
  }

  const items = cart?.items || []

  return (
    <section>
      <div className="section-head">
        <h1>Корзина</h1>
      </div>
      {message && <div className="notice">{message}</div>}
      {items.length === 0 ? (
        <EmptyState title="Корзина пустая" text="Добавьте кофе или выпечку из каталога" />
      ) : (
        <>
          <div className="list">
            {items.map((item) => (
              <div className="list-row" key={item.id}>
                <div>
                  <strong>{item.product.name}</strong>
                  <p>{item.quantity} шт, молоко: {milkLabel(item.milk_type)}</p>
                </div>
                <div className="row-actions">
                  <span>{item.subtotal} ₽</span>
                  <button onClick={() => removeItem(item.id)}>Удалить</button>
                </div>
              </div>
            ))}
          </div>
          <div className="summary">
            <strong>Итого: {cart.total_price} ₽</strong>
            <button onClick={checkout}>Оформить заказ</button>
          </div>
        </>
      )}
    </section>
  )
}

function OrdersPage({ user }) {
  const [orders, setOrders] = useState([])

  useEffect(() => {
    if (user) {
      getOrders().then(setOrders)
    }
  }, [user])

  if (!user) {
    return <EmptyState title="Нужен вход" text="История заказов доступна после входа" />
  }

  return (
    <section>
      <div className="section-head">
        <h1>Заказы</h1>
      </div>
      <div className="list">
        {orders.map((order) => (
          <div className="order-card" key={order.id}>
            <div className="order-title">
              <strong>Заказ №{order.id}</strong>
              <span>{order.status}</span>
            </div>
            <p>{order.total_price} ₽</p>
            {order.items.map((item) => (
              <small key={item.id}>
                {item.product_name} x {item.quantity}, {milkLabel(item.milk_type)}
              </small>
            ))}
          </div>
        ))}
      </div>
    </section>
  )
}

function AuthPage({ onAuth }) {
  const navigate = useNavigate()
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: ''
  })
  const [error, setError] = useState('')

  const title = useMemo(() => (mode === 'login' ? 'Вход' : 'Регистрация'), [mode])

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function submit(event) {
    event.preventDefault()
    setError('')
    try {
      const user = mode === 'login'
        ? await login({ username: form.username, password: form.password })
        : await register(form)
      onAuth(user)
      navigate('/')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <section className="auth-panel">
      <h1>{title}</h1>
      <div className="tabs">
        <button className={mode === 'login' ? 'active' : ''} onClick={() => setMode('login')}>
          Войти
        </button>
        <button className={mode === 'register' ? 'active' : ''} onClick={() => setMode('register')}>
          Создать аккаунт
        </button>
      </div>
      <form onSubmit={submit}>
        <input
          placeholder="Логин"
          value={form.username}
          onChange={(event) => updateField('username', event.target.value)}
        />
        {mode === 'register' && (
          <input
            placeholder="Почта"
            value={form.email}
            onChange={(event) => updateField('email', event.target.value)}
          />
        )}
        <input
          type="password"
          placeholder="Пароль"
          value={form.password}
          onChange={(event) => updateField('password', event.target.value)}
        />
        {error && <div className="error">{error}</div>}
        <button type="submit">{title}</button>
      </form>
    </section>
  )
}

function EmptyState({ title, text }) {
  return (
    <div className="empty">
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
  )
}

function milkLabel(value) {
  return milkOptions.find(([key]) => key === value)?.[1] || value
}

