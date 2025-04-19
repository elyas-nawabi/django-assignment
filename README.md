# 🛠️ Job Processing System API

A Django REST Framework-based backend application for handling job submissions with OTP-based email authentication and asynchronous job processing using **Celery** and **Redis**.

> ✅ Suitable for production-grade workloads and educational use cases.

---

## 🚀 Features

- ✅ User Registration with Email and OTP Verification  
- 🔐 Secure Login with JWT Authentication  
- 🔄 Asynchronous Job Processing with Celery  
- 🧠 Job Scheduling with Celery Beat  
- 📨 Email delivery via console (can be extended to SMTP services)  
- 📊 Job Status Tracking and Result Retrieval  
- 🎯 Role-based Access: Only verified users can create and view their own jobs/results

---

## 🧰 Tech Stack

- **Backend**: Django, Django REST Framework
- **Task Queue**: Celery
- **Message Broker**: Redis
- **Email Verification**: OTP Model
- **Database**: SQLite (easily swappable with PostgreSQL/MySQL)
- **Docs**: drf-spectacular (OpenAPI/Swagger)

---

## 📦 Installation Guide

### ✅ Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/job-processing-system.git
cd job-processing-system
```

### ✅ Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate    # On Windows
# source venv/bin/activate      # On Linux/macOS
```

### ✅ Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuration

### Environment Settings

Edit `.env` or set directly in `settings.py`:

```python
# Email backend for dev
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

### Django Settings

In `settings.py`:

```python
AUTH_USER_MODEL = 'users.CustomUser'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

---

## 🔃 Running the Project

### Step 1: Migrate Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Superuser (optional)

```bash
python manage.py createsuperuser
```

### Step 3: Run Development Server

```bash
python manage.py runserver
```

---

## ⚙️ Running Celery + Beat

### ✅ Start Redis Server

Make sure Redis is installed and running:

```bash
redis-server
```

### ✅ Start Celery Worker

```bash
celery -A job_system worker --loglevel=info
```

### ✅ Start Celery Beat Scheduler (in a separate terminal)

```bash
celery -A job_system beat --loglevel=info
```

> Note: On Windows, `-B` flag **doesn't work**. Run Beat separately as above.

---

## 🌼 Flower (Celery Monitoring)

Install and run:

```bash
pip install flower
celery -A job_system flower
```

Visit: [http://localhost:5555](http://localhost:5555) for real-time task monitoring.

---

## ✅ API Workflow (Step by Step)

1. **Register** → `POST /api/register/`  
2. **Receive OTP on Email Console**
3. **Verify OTP** → `POST /api/verify-otp/`  
4. **Login** → `POST /api/login/` → Receive access & refresh tokens  
5. **Create Job** → `POST /api/jobs/` (requires authentication)  
6. **Background Job Starts Processing Automatically**  
7. **Check Job Status** → `GET /api/jobs/`  
8. **View Results** → `GET /api/job-results/` (if job is complete)

---

## 🛡️ Permissions and Validations

- 🚫 **Jobs** can't be created with `scheduled_time` in the past.
- 🔒 **Only verified users** can access job endpoints.
- 👤 **Users can only access their own jobs and results.**
- 📅 **Results** are only available when jobs are marked as `"completed"`.
- 🧾 OTPs expire after 10 minutes and can't be reused.

---

## 🧪 API Docs

Once server is running:

Visit:  
🔍 [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)  
🧾 or [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

---

## 📂 Project Structure

```
job-processing-system/
├── job_system/           # Django project
│   ├── celery.py         # Celery configuration
│   └── settings.py
├── users/                # Custom User and OTP
├── jobs/                 # Job and JobResult models
├── requirements.txt
├── manage.py
```

---

## 🤝 Contribution Guide

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request.

---

## 📧 Contact

**Author**: Mohammad Elyas Nawabi  
**Email**: elyas.nawabi19@gmail.com  

---

### ⭐ If this project helped you, give it a star on GitHub!