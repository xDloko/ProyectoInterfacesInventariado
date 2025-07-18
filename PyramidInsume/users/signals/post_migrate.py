# users/signals/post_migrate.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_superuser_after_migrate(sender, **kwargs):
    from users.scripts.create_default_admin import run
    run()
