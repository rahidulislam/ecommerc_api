# Ecommerce API Project Structure

```
ecommerc_api
├─ README.md
├─ cart
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ services.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ core
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ tests.py
│  └─ views.py
├─ ecommerce_api
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ base_model.py
│  ├─ permissions.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ manage.py
├─ order
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ services
│  │  ├─ __init__.py
│  │  ├─ order_creation.py
│  │  ├─ order_query.py
│  │  ├─ order_validation.py
│  │  └─ stock_management.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ product
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ filters.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ requirements.txt
└─ users
   ├─ __init__.py
   ├─ admin.py
   ├─ apps.py
   ├─ managers.py
   ├─ models.py
   ├─ serializers.py
   ├─ signals.py
   ├─ tests.py
   ├─ urls.py
   └─ views.py

```
