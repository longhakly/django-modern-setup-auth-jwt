# Django Project

A Django Restful-API service.

## 🚀 Requirements

- Python 3.10+
- pip
- virtualenv (optional but recommended)
- PostgreSQL / SQLite (or your preferred DB)

## 📦 Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/longhakly/Digital-Event-Invitation-API.git
cd Digital-Event-Invitation-API

# 2. Create and activate virtual environment
python -m venv venv
MAC: source venv/bin/activate
Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file and update configs
cp .env.example .env

# 5. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 6. Load seeder data
python manage.py loaddata seeder/role.json

# 7. Create a superuser (optional if not using admin)
python manage.py createsuperuser

# 8. Run the development server
python manage.py runserver
```

### Django App
```bash
python manage.py startapp example_app
```

### Migrations & Database
```bash
# Create migrations based on model changes
python manage.py makemigrations

# Apply all unapplied migrations
python manage.py migrate

# View the migration plan
python manage.py showmigrations

# Fake a migration (mark as applied without running it)
python manage.py migrate --fake your_app

# Reset migrations (DANGEROUS - dev only)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```

### User Management
```bash
# Create a superuser (optional if not using admin)
python manage.py createsuperuser

# Change password for a user
python manage.py changepassword <username>
```
### Debugging & Shell
```bash
# Django interactive shell
python manage.py shell

# With IPython (if installed)
python manage.py shell_plus
```
### Data Management
```bash
# Dump data to JSON
python manage.py dumpdata > data.json

# Dump a specific app/model
python manage.py dumpdata your_app.ModelName > model.json

# Load data from file
python manage.py loaddata data.json
```
### Static & Media Files
```bash
# Collect static files into STATIC_ROOT (for deployment)
python manage.py collectstatic

# Clear static files
python manage.py collectstatic --clear
```