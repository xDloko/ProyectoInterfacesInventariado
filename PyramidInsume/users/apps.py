from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError
        from django.core.management import call_command

        User = get_user_model()

        try:
            if not User.objects.filter(email='admin@example.com').exists():
                print("🛠️ Creando usuario administrador predeterminado...")
                User.objects.create_superuser(
                    email='admin@example.com',
                    password='admin123',
                    user_type=1,  # Administrador
                    ciudad='BOG'
                )
        except (OperationalError, ProgrammingError):
            # Evita errores cuando aún no se ha creado la tabla (por ejemplo, en migrate inicial)
            pass
