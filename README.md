# 🛒 GroceryMS — General Departmental Store Management System

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> A full-stack grocery store management system built with Flask and vanilla JS — featuring product catalogs, cart management, supplier/customer tracking, and a live analytics dashboard.

---

## 📸 Screenshots

### 🏠 Homepage / Hero Banner
![Homepage](screenshots/homepage.png)

### 🛍️ Product Catalog / Shop
![Shop](screenshots/shop.png)

### 🛒 Shopping Cart
![Cart](screenshots/cart.png)

### 📦 Suppliers Table
![Suppliers](screenshots/suppliers.png)

### 👥 Customers Table
![Customers](screenshots/customers.png)

### 📊 Reports Dashboard
![Reports](screenshots/reports.png)

---

## ✨ Features

- 🗂️ **Category Management** — Browse and filter products by category
- 🥦 **75+ Products** — Pre-loaded across 5 categories (Fruits, Vegetables, Dairy, Bakery, Beverages)
- 🛒 **Shopping Cart** — Add items, adjust quantities, remove products per customer
- ✅ **Order Confirmation** — Confirm orders with date stamping
- 🏪 **Supplier Management** — View and add suppliers with full contact details
- 👤 **Customer Management** — Register and manage customers
- 📊 **Reports & Analytics** — Live dashboard showing revenue, top items, pending orders
- 🖼️ **Real Food Images** — Product cards with Unsplash photos + smart fallback
- 🔔 **Toast Notifications** — Success/error feedback on every action
- 📱 **Responsive Design** — Works on desktop and mobile

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask, Flask-CORS |
| Frontend | HTML5, CSS3 (Grid + Flexbox), Vanilla JS |
| Fonts | Google Fonts — Poppins |
| Images | Unsplash API (dynamic) |
| Storage | In-memory (intentional — DSA project) |

> ⚠️ **Note:** All data is stored in-memory and resets on server restart. This is intentional — the project demonstrates OOP/DSA concepts (originally designed in C++) converted to a Python Flask web app.

---

## 🗂️ Project Structure

```
Grocery Management System/
├── app.py                  # Flask backend — all API routes & in-memory data
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Single-page frontend (HTML + CSS + JS)
├── screenshots/            # Add your screenshots here
│   ├── homepage.png
│   ├── shop.png
│   ├── cart.png
│   ├── suppliers.png
│   ├── customers.png
│   └── reports.png
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/GroceryMS.git
cd GroceryMS
```

**2. Install dependencies**
```bash
pip install flask flask-cors
```

**3. Start the Flask server**
```bash
python app.py
```

**4. Open in your browser**
```
http://127.0.0.1:5000
```

That's it — no database setup, no environment variables needed. 🎉

---

## 🔌 API Endpoints

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | List all categories |

### Items / Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items` | List all items |
| GET | `/api/items/<item_id>` | Get a single item |
| POST | `/api/items` | Add a new item |

### Suppliers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/suppliers` | List all suppliers |
| POST | `/api/suppliers` | Add a new supplier |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | List all customers |
| POST | `/api/customers` | Add a new customer |

### Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart/<customer_id>` | View a customer's cart |
| POST | `/api/cart/<customer_id>/add` | Add item to cart `{item_id, qty}` |
| DELETE | `/api/cart/<customer_id>/remove/<item_id>` | Remove item from cart |
| POST | `/api/cart/<customer_id>/confirm` | Confirm order `{day, month, year}` |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reports` | Get analytics summary |

---

## 📦 Pre-loaded Dummy Data

| Resource | Count | Details |
|----------|-------|---------|
| 🗂️ Categories | 5 | Fruits, Vegetables, Dairy, Bakery, Beverages |
| 🛒 Products | 75+ | 15 per category, with prices and stock levels |
| 🏪 Suppliers | 20 | With shop, city, society, item supplied |
| 👥 Customers | 20 | With address, phone, purchase history |

---

## 🎓 Academic Context

This project was developed as a **DSA / OOP semester project** at the University of Lahore.

The core logic was originally written in **C++** using Object-Oriented Programming principles with the following classes:

- `Category` — stores category metadata
- `Item` — product details and stock
- `Supplier` — supplier info and supply schedule
- `Customer` — customer profile and cart reference
- `Cart` — per-customer cart with order management

These were then converted into a **Python Flask REST API** with a **single-page HTML/JS frontend** to make the project interactive and presentable.

---

## 👩‍💻 Developer

**Noor Ul Eman** Software Engineer


---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — feel free to use, modify, and distribute.