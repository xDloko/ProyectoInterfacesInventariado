from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created and instance.is_supervisor:
        # Lógica específica para cuando se crea un promotor
        pass
    
    if created and not instance.is_administrador:
        # Enviar email de bienvenida a usuarios no administradores
        send_mail(
            'Bienvenido a nuestra plataforma',
            'Tu cuenta ha sido creada exitosamente.',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=True,
        )

