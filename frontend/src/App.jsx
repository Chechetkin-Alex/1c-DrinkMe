import { useEffect, useMemo, useState } from 'react'
import { Link, NavLink, Route, Routes, useNavigate, useParams } from 'react-router-dom'

import { getMe, login, logout, register } from './api/auth.js'
import { addCartItem, deleteCartItem, getCart, updateCartItem } from './api/cart.js'
import { getCategories, getProduct, getProducts } from './api/catalog.js'
import { createOrder, getOrders, updateOrder } from './api/orders.js'
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

const sizeLabels = {
  small: 'маленький',
  medium: 'средний',
  large: 'большой',
  none: ''
}

const sizeOrder = {
  small: 1,
  medium: 2,
  large: 3,
  none: 4
}

const orderStatuses = [
  ['created', 'создан'],
  ['paid', 'оплачен'],
  ['in_progress', 'готовится'],
  ['ready', 'готов'],
  ['completed', 'завершен'],
  ['cancelled', 'отменен']
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
  const [comboDrinks, setComboDrinks] = useState([])
  const [comboBakeries, setComboBakeries] = useState([])
  const [category, setCategory] = useState('')
  const [search, setSearch] = useState('')
  const [milkType, setMilkType] = useState('regular')
  const [selectedDrinkVariants, setSelectedDrinkVariants] = useState({})
  const [comboDrinkId, setComboDrinkId] = useState('')
  const [comboBakeryId, setComboBakeryId] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    getCategories().then(setCategories)
    getProducts({ type: 'drink' }).then((items) => {
      const smallDrinks = items.filter((item) => item.drink_size === 'small')
      setComboDrinks(smallDrinks)
      setComboDrinkId(String(smallDrinks[0]?.id || ''))
    })
    getProducts({ type: 'bakery' }).then((items) => {
      setComboBakeries(items)
      setComboBakeryId(String(items[0]?.id || ''))
    })
  }, [])

  useEffect(() => {
    getProducts({ category, search }).then(setProducts)
  }, [category, search])

  const productCards = useMemo(() => {
    const cards = []
    const drinkGroups = new Map()

    products.forEach((product) => {
      if (product.product_type !== 'drink') {
        cards.push({
          key: `product-${product.id}`,
          product,
          variants: [product]
        })
        return
      }

      const key = `drink-${product.category.slug}-${product.name}`
      if (!drinkGroups.has(key)) {
        const group = {
          key,
          product,
          variants: []
        }
        drinkGroups.set(key, group)
        cards.push(group)
      }
      drinkGroups.get(key).variants.push(product)
    })

    return cards.map((card) => ({
      ...card,
      variants: [...card.variants].sort((left, right) => (
        sizeOrder[left.drink_size] - sizeOrder[right.drink_size]
      ))
    }))
  }, [products])

  function selectedProduct(card) {
    if (card.variants.length === 1) {
      return card.product
    }
    const selectedId = Number(selectedDrinkVariants[card.key])
    return card.variants.find((item) => item.id === selectedId) || card.variants[0]
  }

  async function addToCart(card) {
    if (!user) {
      setMessage('Сначала войдите в аккаунт')
      return
    }

    const product = selectedProduct(card)
    const payload = {
      product_id: product.id,
      quantity: 1,
      milk_type: product.product_type === 'drink' ? milkType : 'none'
    }
    if (product.is_student_special) {
      payload.combo_drink_id = Number(comboDrinkId)
      payload.combo_bakery_id = Number(comboBakeryId)
    }
    await addCartItem(payload)
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
        {productCards.map((card) => {
          const product = selectedProduct(card)
          return (
          <article className="product-card" key={card.key}>
            <div className="product-type">{product.category.name}</div>
            <h2>{product.name}</h2>
            {card.variants.length > 1 && (
              <select
                value={product.id}
                onChange={(event) => setSelectedDrinkVariants((current) => ({
                  ...current,
                  [card.key]: event.target.value
                }))}
              >
                {card.variants.map((item) => (
                  <option key={item.id} value={item.id}>
                    {sizeLabel(item.drink_size)}, {item.price} ₽
                  </option>
                ))}
              </select>
            )}
            {product.product_type === 'drink' && card.variants.length === 1 && (
              <span className="muted">{sizeLabel(product.drink_size)}</span>
            )}
            {product.is_student_special && (
              <div className="combo-controls">
                <select value={comboDrinkId} onChange={(event) => setComboDrinkId(event.target.value)}>
                  {comboDrinks.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.name}, {sizeLabel(item.drink_size)}
                    </option>
                  ))}
                </select>
                <select value={comboBakeryId} onChange={(event) => setComboBakeryId(event.target.value)}>
                  {comboBakeries.map((item) => (
                    <option key={item.id} value={item.id}>{item.name}</option>
                  ))}
                </select>
              </div>
            )}
            <div className="card-bottom">
              <strong>{product.price} ₽</strong>
              <div className="card-actions">
                <Link className="secondary-link" to={`/products/${product.id}`}>Открыть</Link>
                <button onClick={() => addToCart(card)}>В корзину</button>
              </div>
            </div>
            {product.is_student_special && <span className="special">студенческое комбо</span>}
          </article>
          )
        })}
      </div>
    </section>
  )
}

function ProductPage({ user }) {
  const { id } = useParams()
  const [product, setProduct] = useState(null)
  const [reviews, setReviews] = useState([])
  const [cartItems, setCartItems] = useState([])
  const [comboDrinks, setComboDrinks] = useState([])
  const [comboBakeries, setComboBakeries] = useState([])
  const [milkType, setMilkType] = useState('regular')
  const [comboDrinkId, setComboDrinkId] = useState('')
  const [comboBakeryId, setComboBakeryId] = useState('')
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

  useEffect(() => {
    getProducts({ type: 'drink' }).then((items) => {
      const smallDrinks = items.filter((item) => item.drink_size === 'small')
      setComboDrinks(smallDrinks)
      setComboDrinkId(String(smallDrinks[0]?.id || ''))
    })
    getProducts({ type: 'bakery' }).then((items) => {
      setComboBakeries(items)
      setComboBakeryId(String(items[0]?.id || ''))
    })
  }, [])

  useEffect(() => {
    if (user) {
      getCart().then((cart) => {
        setCartItems(cart.items)
      })
    } else {
      setCartItems([])
    }
  }, [user])

  const productCartCount = useMemo(() => {
    if (!product) {
      return 0
    }
    return cartItems
      .filter((item) => item.product.id === product.id)
      .reduce((sum, item) => sum + item.quantity, 0)
  }, [cartItems, product])

  async function addToCart() {
    if (!user) {
      setError('Сначала войдите в аккаунт')
      return
    }

    const payload = {
      product_id: product.id,
      quantity: 1,
      milk_type: product.product_type === 'drink' ? milkType : 'none'
    }
    if (product.is_student_special) {
      payload.combo_drink_id = Number(comboDrinkId)
      payload.combo_bakery_id = Number(comboBakeryId)
    }
    await addCartItem(payload)
    const cart = await getCart()
    setCartItems(cart.items)
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
      setMessage('Отзыв сохранен')
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
          {product.product_type === 'drink' && <span className="muted">{sizeLabel(product.drink_size)}</span>}
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
          {product.is_student_special && (
            <>
              <label>
                Кофе
                <select value={comboDrinkId} onChange={(event) => setComboDrinkId(event.target.value)}>
                  {comboDrinks.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.name}, {sizeLabel(item.drink_size)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Выпечка
                <select value={comboBakeryId} onChange={(event) => setComboBakeryId(event.target.value)}>
                  {comboBakeries.map((item) => (
                    <option key={item.id} value={item.id}>{item.name}</option>
                  ))}
                </select>
              </label>
            </>
          )}
          <span className="cart-counter">В корзине этого товара: {productCartCount}</span>
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
                  {item.product.product_type === 'drink' && (
                    <p>{sizeLabel(item.product.drink_size)}</p>
                  )}
                  {item.product.is_student_special && (
                    <p>
                      {item.combo_drink?.name}, {sizeLabel(item.combo_drink?.drink_size)}
                      {' + '}
                      {item.combo_bakery?.name}
                    </p>
                  )}
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

  async function changeStatus(order, status) {
    const updatedOrder = await updateOrder(order.id, { status })
    setOrders((current) => current.map((item) => (
      item.id === updatedOrder.id ? updatedOrder : item
    )))
  }

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
                {user.is_staff ? (
                  <select value={order.status} onChange={(event) => changeStatus(order, event.target.value)}>
                    {orderStatuses.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                ) : (
                  <span>{statusLabel(order.status)}</span>
                )}
              </div>
              <p>Заказал: {order.username}</p>
              <p>Время: {formatDate(order.created_at)}</p>
              <p>{order.total_price} ₽</p>
              {order.items.map((item) => (
                <small key={item.id}>
                  {item.product_name} x {item.quantity}, {milkLabel(item.milk_type)}
                  {item.combo_drink_name && `, ${item.combo_drink_name} + ${item.combo_bakery_name}`}
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

function sizeLabel(value) {
  return sizeLabels[value] || ''
}

function statusLabel(value) {
  return orderStatuses.find(([key]) => key === value)?.[1] || value
}

function formatDate(value) {
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(value))
}
