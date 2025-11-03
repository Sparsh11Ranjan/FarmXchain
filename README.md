# 🌾 FarmXchain — Smart Agricultural Marketplace Backend

🚀 **FarmXchain** is a Flask-based backend platform designed to revolutionize how farmers and buyers connect.  
It provides a robust API for **farmer registration**, **product management**, **farming type categorization**, **action logging**, and **secure authentication** — empowering a smarter, data-driven agricultural ecosystem.

---

## 🧠 Overview

FarmXchain focuses on **backend architecture**, providing a clean and scalable server-side system for an agricultural marketplace.

### 🎯 Core Objectives
- Digitize the connection between **farmers** and **buyers**.
- Provide a **secure and scalable backend API**.
- Automate **data records, product management, and farmer actions**.
- Support **real-time synchronization** with a React-based frontend.

---

## 🏗️ Features

| Feature | Description |
|----------|-------------|
| 👨‍🌾 **Farmer Management** | Register, update, or delete farmers. Store Aadhaar, contact, and farming type details. |
| 🛒 **Agro Product Listings** | Farmers can list products with name, price, and description. |
| 🌱 **Farming Type Management** | Manage and categorize different farming practices (e.g., Dairy, Poultry, Organic). |
| 🧾 **Action Records (Triggers)** | Every insert/update/delete on farmer data is automatically logged in the `trig` table. |
| 🔐 **Authentication System** | JWT-based secure login and signup (with password hashing via bcrypt). |
| 💾 **MySQL Database Integration** | Efficient relational schema with normalized tables and triggers. |
| 🔗 **RESTful API Design** | Modular API endpoints grouped into blueprints. |
| 🌐 **CORS-Enabled API** | Allows frontend (React at `localhost:3000`) to interact securely. |
| 🧩 **Factory Pattern Architecture** | Flexible, testable Flask app creation using the factory design pattern. |

---

## ⚙️ Tech Stack

| Layer | Technologies |
|--------|---------------|
| **Language** | Python 3.x |
| **Framework** | Flask |
| **Database** | MySQL (with PyMySQL driver) |
| **ORM** | SQLAlchemy |
| **Authentication** | Flask-JWT-Extended, bcrypt |
| **Migrations** | Flask-Migrate (Alembic) |
| **Validation** | Marshmallow |
| **Configuration** | python-dotenv |
| **Cross-Origin Support** | Flask-CORS |

---

## 🧩 Project Structure

FarmXchain/
│
├── app.py # Application factory (sets up Flask app, config, blueprints)
├── manage.py # CLI runner for server & migrations
├── models.py # SQLAlchemy models (Register, Products, Farming, Trig, User)
├── schemas.py # Marshmallow schemas for validation
│
├── routes/
│ ├── auth.py # User registration & JWT authentication
│ ├── farmers.py # CRUD routes for farmers
│ ├── products.py # CRUD routes for agro products
│ ├── farming.py # CRUD routes for farming types
│ ├── records.py # API for fetching activity logs
│
├── migrations/ # Auto-generated migration files (via Flask-Migrate)
│
├── .env.example # Environment variable template
├── requirements.txt # Project dependencies
└── README.md # This file


---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/FarmXchain.git
cd FarmXchain
