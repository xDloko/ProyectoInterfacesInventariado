# users/scripts/create_default_admin.py

from django.contrib.auth import get_user_model
import os

def run():
    User = get_user_model()
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(
            email=email,
            password=password,
            user_type=1,  # Administrador
            ciudad='BOG'
        )
        print(f"✅ Superusuario '{email}' creado.")
    else:
        print(f"ℹ️ Superusuario '{email}' ya existe.")
