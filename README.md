# 🎫 Chali Event Management System

A feature-rich Django-powered event management platform built for organizers and attendees. It supports event creation, ticket purchasing, role-based user access, and mobile payments via M-Pesa STK Push.

---

## 🚀 Features

- 🔐 User authentication (register/login/logout)
- 🎭 Role-based users: Organizers vs Attendees
- 📝 Organizers can create, edit, delete events
- 🎟️ Ticketing system with real-time inventory
- 💳 M-Pesa STK Push integration
- 🧾 CSV export of attendees per event
- 📅 Calendar view of upcoming events
- 📊 Organizer dashboard showing event stats
- ✉️ Email confirmations on registration and payments

---

## 📦 Technologies Used

- **Backend:** Django 5.2+
- **Database:** SQLite3 (switchable to PostgreSQL)
- **Auth:** Django's built-in system with extended forms
- **Styling:** Bootstrap 5, custom CSS
- **Payments:** Safaricom M-Pesa STK Push API
- **Email:** Django console backend (ready for SMTP)

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/yourusername/chali-event-management.git
cd chali-event-management
```

### 2. Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Configure Django Settings

```
MPESA_CONSUMER_KEY = 'your-consumer-key'
MPESA_CONSUMER_SECRET = 'your-consumer-secret'
MPESA_PASSKEY = 'your-lipa-na-mpesa-passkey'
MPESA_SHORTCODE = '174379'
CALLBACK_URL = 'https://yourdomain.com/mpesa/callback/'
```

### 5. Apply Migrations

```
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```
python manage.py createsuperuser
```

## 🌐 Running Locally

```
python manage.py runserver
```

Open your browser at: `http://127.0.0.1:8000/`

## 💳 Simulating M-Pesa Payments

- Use test number: 254708374149
- Make sure Shortcode and Passkey are valid for sandbox
- Use Ngrok for local webhook testing: