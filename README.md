# 🛒 phiMart – E-commerce API

**phiMart** is a fully functional **E-commerce REST API** built with **Django Rest Framework (DRF)**.
It provides endpoints for products, categories, carts, and orders, with **JWT authentication** using **Djoser** and **interactive API documentation** via **Swagger (drf_yasg)**.

---

## 🚀 Features

- **Authentication & Authorization**

  - JWT Authentication (Login, Register, Refresh, Logout)
  - User management with Djoser

- **Products & Categories**

  - CRUD operations for products
  - Organized by categories
  - Product images with file size validation

- **Cart & Orders**

  - Add/Remove products from cart
  - Manage customer orders
  - Cart linked with users

- **API Documentation**

  - Swagger UI (`/swagger/`)
  - Redoc (`/redoc/`)

- **Optimized & Secure**

  - Query optimizations with `select_related` and `prefetch_related`
  - Permissions and authentication checks

---

## 🛠️ Tech Stack

- **Backend:** Django, Django Rest Framework (DRF)
- **Authentication:** JWT (Djoser + SimpleJWT)
- **Database:** PostgreSQL (or SQLite for dev)
- **API Docs:** drf_yasg (Swagger & Redoc)

---

## 📂 Project Structure

```
phiMart/
│── ecommerce/          # Main Django project
│── product/            # Products & Categories app
│── order/              # Orders & Cart app
│── users/              # User authentication & profiles
│── requirements.txt    # Dependencies
│── manage.py
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/phiMart.git
   cd phiMart
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Mac/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

---

## 🔑 Authentication (JWT)

- **Register:** `POST /auth/users/`
- **Login (get tokens):** `POST /auth/jwt/create/`
- **Refresh token:** `POST /auth/jwt/refresh/`
- **Get current user:** `GET /auth/users/me/`

## 📖 API Documentation

- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **Redoc:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## 📌 Example Endpoints

- **Products**

  - `GET /api/products/` → List all products
  - `POST /api/products/` → Create new product (admin only)
  - `GET /api/products/{id}/` → Retrieve product by ID

- **Categories**

  - `GET /api/categories/` → List categories
  - `POST /api/categories/` → Create category (admin only)

- **Cart**

  - `POST /api/cart/add/` → Add item to cart
  - `GET /api/cart/` → View user’s cart

- **Orders**

  - `POST /api/orders/` → Place an order
  - `GET /api/orders/` → User’s order history

---

## 🧪 Testing

Run unit tests:

```bash
python manage.py test
```

## 👨‍💻 Author

- **Joynul Islam**
  📧 \[joynul8763@gmail.com]
  🌐 \[https://github.com/JoynulIslam]

---

⚡ **phiMart** – Scalable and secure e-commerce API for modern applications.

---
