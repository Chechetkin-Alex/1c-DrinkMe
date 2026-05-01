import { useEffect, useMemo, useState } from 'react'
import { Link, NavLink, Route, Routes, useNavigate, useParams } from 'react-router-dom'

import { getMe, login, logout, register } from './api/auth.js'
import { addCartItem, deleteCartItem, getCart, updateCartItem } from './api/cart.js'
import { getCategories, getProduct, getProducts } from './api/catalog.js'
import { createOrder, getOrders } from './api/orders.js'
import { getToken } from './api/client.js'
import { createProductReview, getProductReviews } from './api/reviews.js'

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
          <Route path="/products/:id" element={<ProductPage user={user} />} />
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
              <div className="card-actions">
                <Link className="secondary-link" to={`/products/${product.id}`}>Открыть</Link>
                <button onClick={() => addToCart(product)}>В корзину</button>
              </div>
            </div>
            {product.is_student_special && <span className="special">студенческое комбо</span>}
          </article>
        ))}
      </div>
    </section>
  )
}

function ProductPage({ user }) {
  const { id } = useParams()
  const [product, setProduct] = useState(null)
  const [reviews, setReviews] = useState([])
  const [milkType, setMilkType] = useState('regular')
  const [reviewForm, setReviewForm] = useState({
    rating: 5,
    text: ''
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    getProduct(id).then(setProduct)
    getProductReviews(id).then(setReviews)
  }, [id])

  async function addToCart() {
    if (!user) {
      setError('Сначала войдите в аккаунт')
      return
    }

    await addCartItem({
      product_id: product.id,
      quantity: 1,
      milk_type: product.product_type === 'drink' ? milkType : 'none'
    })
    setMessage('Товар добавлен в корзину')
    setError('')
  }

  async function submitReview(event) {
    event.preventDefault()
    if (!user) {
      setError('Сначала войдите в аккаунт')
      return
    }

    try {
      await createProductReview(id, {
        rating: Number(reviewForm.rating),
        text: reviewForm.text
      })
      setReviews(await getProductReviews(id))
      setReviewForm({ rating: 5, text: '' })
      setMessage('Отзыв добавлен')
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  if (!product) {
    return <div>Загрузка</div>
  }

  return (
    <section>
      <Link className="back-link" to="/">Назад в каталог</Link>
      <div className="product-detail">
        <div>
          <div className="product-type">{product.category.name}</div>
          <h1>{product.name}</h1>
          <p>{product.description || 'Описание появится позже'}</p>
          {product.is_student_special && <span className="special">студенческое комбо</span>}
        </div>

        <aside className="buy-panel">
          <strong>{product.price} ₽</strong>
          {product.product_type === 'drink' && (
            <label>
              Молоко
              <select value={milkType} onChange={(event) => setMilkType(event.target.value)}>
                {milkOptions.map(([value, label]) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </select>
            </label>
          )}
          <button onClick={addToCart}>В корзину</button>
        </aside>
      </div>

      {message && <div className="notice">{message}</div>}
      {error && <div className="error">{error}</div>}

      <div className="reviews-layout">
        <section>
          <h2>Отзывы</h2>
          {reviews.length === 0 ? (
            <p>Отзывов пока нет</p>
          ) : (
            <div className="list">
              {reviews.map((review) => (
                <div className="review-card" key={review.id}>
                  <strong>{review.username}</strong>
                  <span>{review.rating} из 5</span>
                  <p>{review.text || 'Без текста'}</p>
                </div>
              ))}
            </div>
          )}
        </section>

        <form className="review-form" onSubmit={submitReview}>
          <h2>Оставить отзыв</h2>
          <select
            value={reviewForm.rating}
            onChange={(event) => setReviewForm((current) => ({
              ...current,
              rating: event.target.value
            }))}
          >
            <option value="5">5</option>
            <option value="4">4</option>
            <option value="3">3</option>
            <option value="2">2</option>
            <option value="1">1</option>
          </select>
          <textarea
            placeholder="Текст отзыва"
            value={reviewForm.text}
            onChange={(event) => setReviewForm((current) => ({
              ...current,
              text: event.target.value
            }))}
          />
          <button type="submit">Отправить</button>
        </form>
      </div>
    </section>
  )
}

function CartPage({ user }) {
  const [cart, setCart] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    if (user) {
      getCart().then(setCart)
    }
  }, [user])

  async function removeItem(id) {
    await deleteCartItem(id)
    setCart(await getCart())
  }

  async function changeQuantity(item, quantity) {
    setError('')
    if (quantity < 1) {
      await removeItem(item.id)
      return
    }

    try {
      await updateCartItem(item.id, { quantity })
      setCart(await getCart())
    } catch (err) {
      setError(err.message)
    }
  }

  async function checkout() {
    setError('')
    try {
      const order = await createOrder()
      setCart(await getCart())
      setMessage(`Заказ №${order.id} создан`)
    } catch (err) {
      setError(err.message)
    }
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
      {error && <div className="error">{error}</div>}
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
                  <div className="stepper" aria-label="Количество">
                    <button onClick={() => changeQuantity(item, item.quantity - 1)}>-</button>
                    <span>{item.quantity}</span>
                    <button onClick={() => changeQuantity(item, item.quantity + 1)}>+</button>
                  </div>
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
      {orders.length === 0 ? (
        <EmptyState title="Заказов пока нет" text="Оформите первый заказ из корзины" />
      ) : (
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
      )}
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
