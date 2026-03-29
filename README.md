
---

# 🚀 ElectroMart – Electronics E-commerce Web Application

ElectroMart is a full-stack e-commerce web application built using Django that enables users to browse, explore, and purchase electronic products online. It offers a seamless shopping experience with product filtering, cart management, and secure payment integration.

---

## 🌟 Features

* 🏠 Dynamic homepage with featured products
* 📱 Electronics product catalog (mobiles, laptops, accessories, etc.)
* 🔍 Product search and category-based filtering
* 📄 Individual product detail page
* 🛒 Add to cart and cart management
* 💳 Secure checkout system
* 💰 Online payment integration using Razorpay
* 🔐 User authentication (Register/Login)
* 📱 Fully responsive user interface

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Payment Gateway:** Razorpay
* **Tools:** Git, GitHub

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd electromart
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configuration

* Ensure `settings.py` is properly configured
* Add Razorpay API keys in settings
* Set `DEBUG = True` for development
* Configure `ALLOWED_HOSTS` if required

### 6. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Server

```bash
python manage.py runserver
```

### 9. Access the Application

* 🌐 Home: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📂 Project Structure

* **ElectroMart/**: Main project configuration, settings, and URL routing
* **WebApp/**: Core application handling product listing, filtering, cart, and user interactions
* **AdminApp/**: Custom admin panel for managing products, users, and orders
* **media/**: Stores uploaded product images and files
* **static/**: Contains global CSS, JavaScript, and frontend assets

---
