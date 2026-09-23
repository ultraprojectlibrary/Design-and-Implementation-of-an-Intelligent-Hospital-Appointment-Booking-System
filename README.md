# Intelligent Hospital Appointment Booking System

A modern, responsive, and robust hospital appointment booking platform built with Django.

## Features
- **Role-based Access Control**: Separate experiences for Patients, Doctors, and Administrators.
- **Intelligent Scheduling**: Dynamic time slot generation based on doctor availability, breaks, and existing appointments. Recommends the earliest available alternative if a slot is fully booked.
- **Double-booking Prevention**: Uses database transaction locking (`select_for_update()`) to prevent race conditions during concurrent bookings.
- **Automated Notifications**: Idempotent Django management command for 24-hour and 2-hour appointment reminders.
- **Responsive UI/UX**: Custom-designed medical UI system with CSS variables, fully mobile-responsive (down to 375px).

## Project Setup (Local Development)

### Prerequisites
- Python 3.10+
- SQLite (default) or PostgreSQL

### 1. Installation
Clone the repository and set up a virtual environment:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Copy `.env.example` to `.env` and fill in your secrets (especially the SMTP email credentials).
```bash
cp .env.example .env
```

### 3. Database Migration
Apply the migrations to set up the database structure:
```bash
python manage.py migrate
```

### 4. Seed Demo Data
Populate the database with realistic test departments, doctors (and their schedules), and a test patient:
```bash
python manage.py seed_db
```
*Note: This creates doctors (e.g., username `drsmith` / password `password123`) and a patient (`patient1` / `password123`).*

### 5. Create Administrator
Create a superuser to access the Django Admin interface at `/admin/`:
```bash
python manage.py createsuperuser
```

### 6. Run Server
Start the development server:
```bash
python manage.py runserver
```

### 7. Run Reminders (Background Task)
To test the reminder system, run the management command. It will find upcoming appointments and send emails via Django's SMTP backend.
```bash
python manage.py send_appointment_reminders
```

---

## PythonAnywhere Deployment

This application is architected to run seamlessly on PythonAnywhere without requiring Redis, Celery, or complex infrastructure.

1. **Upload Code**: Clone your repo or upload files to your PythonAnywhere account.
2. **Virtual Environment**: Create a virtualenv via the PythonAnywhere console and `pip install -r requirements.txt`.
3. **Web Tab Configuration**:
   - Add your Virtualenv path.
   - Point the WSGI file to your `config/wsgi.py`.
   - Set up Static Files (`/static/` -> `/home/yourusername/hospital_booking/staticfiles`).
4. **Environment Variables**: Add your `.env` variables (including database/email credentials) to the `wsgi.py` file using `python-dotenv`.
5. **Scheduled Tasks (Cron)**: 
   To automate email reminders, go to the **Tasks** tab in PythonAnywhere and create a new scheduled task that runs periodically (e.g., hourly):
   ```bash
   /home/yourusername/.virtualenvs/myvenv/bin/python /home/yourusername/hospital_booking/manage.py send_appointment_reminders
   ```
   *The command is idempotent and will not send duplicate emails for the same reminder type.*
