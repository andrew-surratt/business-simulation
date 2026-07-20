# Business Simulation

## Start

`python manage.py runserver`

Site is available at http://localhost:8000/

## Migrate DB

If needed, update migrations:

`python manage.py makemigrations`

Run migration:

`python manage.py migrate`

## Admin
Admin site is available at http://localhost:8000/admin/

### Create Admin Superuser

`python manage.py createsuperuser`

### Change Password

`python manage.py changepassword <username>`