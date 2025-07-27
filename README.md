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
- Use [Ngrok](https://ngrok.com) for local webhook testing:

```
ngrok http 8000
```

## 🛡️ Security Notes

- M-Pesa credentials should be stored in `.env` in production.
- Always set `DEBUG = False` when deploying.
- Use `HTTPS` for production.
- Use `ALLOWED_HOSTS` and `HTTPS` when going live.

- Use `CSRF` protection.

## 📁 App Structure

```
chali_event_management/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    ├── asgi.py
accounts/
    ├── migrations/
    ├── templates/accounts/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── admin.py
    ├── urls.py
    ├── forms.py
    ├── apps.py
    ├── tests.py
events/
    ├── migrations/
    ├── templates/events/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── admin.py
    ├── urls.py
    ├── forms.py
    ├── apps.py
    ├── tests.py
templates/
    ├── base.html
media/
    ├── event_images/
├── manage.py
├── README.md
├── requirements.txt
```

## 🪄 Future Enhancements

- 🛒 PayPal/Flutterwave integration.
- 🎫 QR code ticket generation.
- 📉 Dashboard analytics for organizers.
- 📝 Ticket tiers (VIP, Regular, Early Bird).

## 📮 Contact & Credits

Built by:

-  [Zablon Zambagarrah](https://github.com/Zambagarrah)
-  [Avril Diamond](https://github.com/almasi-y/)
-  [Lisa Mosweta](https://github.com/lisamswt/)
-  [Mulky Mohammed](https://github.com/mulkymma/)
-  [Ummi Ramma]()


