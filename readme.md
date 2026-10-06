# D-Mart

## Industrial Multi-Vendor E-Commerce Marketplace

D-Mart is an industrial-focused multi-vendor e-commerce web application designed to connect buyers with multiple sellers through a single online marketplace.

The platform allows sellers to publish and manage their industrial products, while buyers can browse products, search for items, add products to their cart, place orders, make payments, and track their purchases.

D-Mart also provides administrative tools for managing sellers, buyers, products, orders, and the overall marketplace.

---

## Project Objective

The main objective of D-Mart is to develop a secure, scalable, and user-friendly online marketplace specifically designed for industrial and commercial products.

The system aims to simplify the process of:

* Buying industrial products online
* Selling products through multiple sellers
* Managing products and stock
* Managing customer orders
* Processing online and cash-on-delivery payments
* Monitoring marketplace activities
* Providing useful sales and demand analytics

---

## User Roles

D-Mart supports three main user roles.

### 1. Admin

The administrator manages and monitors the entire marketplace.

Admin responsibilities include:

* Manage buyers and sellers
* Approve or reject seller accounts
* Block or unblock users
* Manage product categories
* Monitor products
* Monitor orders and payments
* View marketplace statistics
* Monitor seller performance
* Analyze market and product demand

### 2. Seller

Sellers can operate their own businesses through the D-Mart marketplace.

Seller features include:

* Seller registration
* Admin approval system
* Add products
* Edit products
* Delete products
* Manage product stock
* Manage product categories
* View their own orders
* Monitor sales and revenue
* View top-selling products
* Analyze product demand

Sellers can also purchase products from other sellers as normal buyers.

### 3. Buyer

Buyers can use D-Mart to discover and purchase products.

Buyer features include:

* User registration
* Secure login
* Browse products
* Search products
* Browse by category
* View product details
* Add products to cart
* Manage cart quantities
* Checkout
* Place orders
* Make online payments
* Cash on Delivery
* Track orders
* Review and rate products

---

## Payment System

D-Mart supports two payment methods:

### Online Payment

Buyers can pay for their orders through an online payment gateway.

A failed online payment must not be treated as a successful payment.

### Cash on Delivery

Buyers can choose Cash on Delivery when available.

For COD orders, a delivery OTP verification mechanism is planned to provide additional security during delivery.

---

## Order Management

D-Mart follows a structured order lifecycle:

```text
Pending
   ↓
Processing
   ↓
Shipped
   ↓
Delivered
```

The system is designed to maintain accurate order and payment states throughout the process.

---

## Seller Analytics

D-Mart includes a seller analytics system designed to help sellers understand their business performance.

Analytics include:

* Daily sales
* Weekly sales
* Monthly sales
* Revenue
* Order count
* Top-selling products
* Product performance
* Current product demand
* Stock status

The demand analysis can consider factors such as:

* Product views
* Product searches
* Cart additions
* Orders
* Sales
* Current stock

These factors can be used to classify product demand as:

```text
HIGH
MEDIUM
LOW
```

---

## Admin Analytics

The admin can monitor the overall marketplace through centralized analytics.

Planned marketplace analytics include:

* Total buyers
* Total sellers
* Total products
* Total orders
* Overall sales
* Marketplace revenue
* Top sellers
* Top products
* Category performance
* Market demand
* Sales trends

---

## Security

Security is an important part of the D-Mart system.

The application is designed to include:

* Role-based access control
* Secure authentication
* Password hashing through Django
* CSRF protection
* Seller approval before selling
* Order and payment status validation
* Delivery OTP verification for COD
* Protection of sensitive buyer and seller information
* Prevention of unauthorized page access

---

## Technology Stack

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite during development

### Additional Technologies

* Django Authentication
* Django ORM
* Pillow for product image handling
* Git
* GitHub

---

## Project Structure

```text
D-Mart/
│
├── manage.py
│
├── industrial_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── products/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── orders/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── home.html
│   ├── admin/
│   └── accounts/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── db.sqlite3
```

---

## Current Development Status

The project is being developed in phases.

### Completed

* Django project setup
* Virtual environment setup
* SQLite database setup
* Custom user model
* Buyer and seller roles
* Seller profile
* Seller approval system
* Authentication system
* Buyer registration
* Seller registration
* Common login system
* Custom admin login page
* Product and category models
* Product image support
* Admin product management
* Public D-Mart home page
* Database-driven active product display

### In Development

* Product details
* Shopping cart
* Buyer dashboard
* Seller dashboard
* Order management
* Online payment
* COD and delivery OTP
* Seller analytics
* Admin analytics
* Security hardening
* Testing
* Responsive UI improvements

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd D-Mart
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install django pillow
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver 8001
```

Open:

```text
http://127.0.0.1:8001/
```

Admin panel:

```text
http://127.0.0.1:8001/admin/
```

---

## Future Improvements

Future development may include:

* Advanced product search
* Product filtering and sorting
* Shopping cart improvements
* Wishlist
* Buyer dashboard
* Seller dashboard
* Real-time order tracking
* Online payment gateway integration
* COD delivery OTP
* Sales and demand charts
* Advanced marketplace analytics
* Email notifications
* Mobile-responsive improvements
* Production database configuration
* Deployment and performance optimization

---

## Developer

**Dajiv Uthayakumar**

D-Mart is developed as an industry-oriented software development project to demonstrate practical skills in web application development, database management, authentication, e-commerce functionality, and business analytics.
