from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Ensure the signals module exists and is correctly referenced
        try:
            import users.signals.post_migrate  # Conecta la señal después de migrar
        except ModuleNotFoundError:
            pass  # Optionally, log a warning or handle the missing module
