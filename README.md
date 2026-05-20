# Personal Expense Tracker API

A secure, well-structured, tech-stack agnostic REST API built to power a personal finance management application. This system isolates user data natively at the database level, incorporates full token-based JWT authentication, provides detailed analytical insights, and self-documents dynamically via OpenAPI/Swagger specs.

- **Live API URL**: `https://tracker-36la.onrender.com/`
- **Interactive Swagger Documentation**: `https://tracker-36la.onrender.com/docs/`

---

## 🛠️ Tech Stack & Justification

- **Framework**: Python / Django + Django REST Framework (DRF)
- **Authentication**: `django-rest-framework-simplejwt` (JSON Web Tokens)
- **Database**: SQLite (Local development) / PostgreSQL (Production)
- **Documentation**: `drf-spectacular` (OpenAPI 3.0 / Swagger UI)
- **Testing**: `pytest` + `pytest-django`

### Why Django?
1. **Batteries-Included Security**: Django provides absolute defense against SQL injection, XSS, and CSRF vulnerabilities by default. It manages robust password hashing natively using `PBKDF2` with a SHA256 signature without requiring clumsy external logic.
2. **Absolute Data Isolation**: Leveraging Django's powerful Object-Relational Mapper (ORM), we can override the query resolution flow (`get_queryset`) on endpoints. This guarantees programmatically that no user can accidentally view, mutate, or destroy data belonging to another account.
3. **Rapid Development**: The ecosystem natively supports advanced automated schema mapping. This allowed the auto-generation of highly detailed, interactive Swagger documentation directly from serializers and models within a tight 2-day delivery window.

---
### The Quick Way (Automated)
If you are on macOS or Linux (Ubuntu), you can use the shortcut command to create the virtual environment, install dependencies, run migrations, seed data, and start the server all at once:

```bash
make
```

---

## 🚀 Local Installation & Setup

Follow these simple steps to run the environment locally in under 2 minutes:

### 1. Clone the Repository & Initialize Environment
```bash
git clone https://github.com/nitinkumarhere/tracker.git
cd tracker

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install all locked dependencies
pip install -r requirements.txt
```

### 2. Prepare Database & Seed Global Categories
```bash
# Generate structural migrations and run initial schema building
python manage.py makemigrations
python manage.py migrate

# Seed required baseline default system finance categories
python manage.py seed_categories
```

### 3. Generate Realistic Sandbox Analytics Mock Data (Optional)
To test the analytics summary graphs and transaction lists instantly without manual typing, seed the system with a complete pre-configured history profile:
```bash
python manage.py seed_data
```
*Creates user `demo@example.com` with password `password123` containing 100 random multi-category transactions over the past 90 days.*

### 4. Fire Up the Server
```bash
python manage.py runserver
```
Your local server instance is now live at **`http://localhost:8000/`**. 
Access interactive API validation playground directly via **`http://localhost:8000/docs/`**.

---

## 🧪 Running Automation Tests

The backend includes full integration assertions for authentication routines and cross-user data boundary protection policies using `pytest`.

Run the suite locally with a single command:
```bash
pytest
```

---

## ⚙️ Environment Variables

The project reads environment parameters dynamically in production. For local development, fallback defaults are provided automatically.


| Variable Name | Purpose / Target | Production Value Example            |
| :--- | :--- |:------------------------------------|
| `DJANGO_DEBUG` | Switches verbosity error modes | `False`                             |
| `DJANGO_SECRET_KEY` | Cryptographic signature validation token | *Generate long random string*       |
| `ALLOWED_HOSTS` | Array of authorized domain endpoints | `https://tracker-36la.onrender.com`                                  |
| `DATABASE_URL` | Cloud structural PostgreSQL link string | `postgres://user:pass@host:port/db` |

---

## 💡 System Design Assumptions & Trade-offs

### 1. Categories Deletion & Cascade Policy
* **Assumption**: If a user creates a custom category, records a transaction against it, and later chooses to delete that category, what happens to their logs? 
* **Design Choice**: We utilize `models.PROTECT` on the Transaction schema's Category foreign key. The system will cleanly block attempts to delete a category if it is currently tied to transactions, forcing the user to reassign their transactions first. This preserves historical analytics bookkeeping accurately.

### 2. Token Blacklisting Omission
* **Trade-off**: To maintain high-speed request processing under the 2-day timeline, tokens are validated cryptographically statelessly via public keys rather than maintaining an active cache database blacklist for logouts. Logouts are handled gracefully client-side by purging tokens from storage, while token expiration is constrained tightly to a 60-minute active lifetime.

---

## 📈 Future Enhancements (With More Time)

If granted additional development iterations, the following production features would be integrated:
1. **Redis Cache Layer & Rate Limiting**: Implement strict throttling policies (`django-ratelimit`) on `/api/auth/login/` and `/register/` endpoints to protect against automated dictionary brute-force attacks.
2. **Bulk Transaction Upload Engine**: Add a multi-part file endpoint to parse CSV or bank statement JSON files asynchronously using Celery worker queues to safely process large data uploads without locking up HTTP execution threads.
3. **Database Index Optimizations**: Add an explicit database index to the composite lookup matching `['user', 'date']` within the `Transaction` table layout to ensure that sub-second response times are maintained as user transaction records grow into millions.
