# Installation and Configuration

Prerequisites: Python 3.11+ compatible with Django 5.2, Git, and a terminal; SQLite works for development. PostgreSQL is optional.

```powershell
git clone https://github.com/miormuhammadamir/assetops.git
cd assetops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_DEBUG="1"
python manage.py migrate
python manage.py setup_roles
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```

The above `git clone` gets GitHub's main branch, not necessarily the source package accompanying this documentation. For this package, extract into a new folder and follow the commands starting at `python -m venv`.

Log in at `http://127.0.0.1:8000/`. For admin accounts open `/admin/`.

Avoid setting DEBUG=1 on internet-accessible servers. Do not store real credentials in Git. Configure secret and hosts through environment variables for nondebug operation.
