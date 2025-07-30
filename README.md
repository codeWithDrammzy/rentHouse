# 🏠 Soni House Agent

**Soni House Agent** is a Django-based rental management system that helps real estate agents or property administrators manage landlords, properties, and tenants in an efficient and organized manner. The platform also allows users (prospective tenants) to search for available rental properties and connect with agents.

---

## 🔁 Project Flow

1. **Admin or Agent logs in**
2. **Registers Landlords** with necessary details (ID card, contact info, etc.)
3. **Adds House Listings** under a specific landlord
4. **Assigns Tenants** to available houses
5. **Payment is calculated** automatically based on selected payment option (6 months or 1 year)
6. **Property availability is updated** based on tenancy
7. **User can search** and view available properties (only those marked as available)

---

## 🏗️ Models Overview

### 👤 Landlord

- Fields: `first_name`, `last_name`, `email`, `phone_number`, `address`, `id_card`
- Soft delete supported via `is_deleted`
- Relationship: A landlord can own multiple houses

### 🏠 House

- Fields: `title`, `description`, `price`, `location`, `num_bedrooms`, `num_bathrooms`, `is_available`, `image`
- Linked to: `Landlord`
- Automatically marked unavailable once a tenant is assigned
- Soft delete supported

### 👥 Tenant

- Fields: `first_name`, `last_name`, `id_card`, `phone_number`, `payment_option`, `last_payment_date`, `payment_amount`, `has_paid`
- Linked to a single house (`OneToOneField`)
- Auto-calculates rent cost based on selected duration
- Tracks payment status (`paid`, `due_soon`, `overdue`)
- Soft delete supported

---

## 💡 Key Features

- 🔐 Agent/Admin authentication
- 🧑‍💼 Landlord management
- 🏘 Property listing with images and status
- 👥 Tenant assignment and rent tracking
- 💰 Dynamic rent calculation (6-months / 1-year)
- 🕵️ Public search for available houses
- 🗑 Soft delete functionality (bin & restore supported)
- 📆 Payment status tracking (`paid`, `due soon`, `overdue`)

---

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (you can switch to PostgreSQL/MySQL)
- **Frontend**: HTML5, Tailwind CSS (or your preferred styling)
- **Media**: Django `ImageField` for property photos
- **Admin Panel**: Django Admin (can be customized)

---

## 🖥️ Installation Guide

```bash
# Clone the project
git clone https://github.com/yourusername/soni-house-agent.git
cd soni-house-agent

# Create virtual environment & activate
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver
