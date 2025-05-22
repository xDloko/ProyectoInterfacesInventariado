from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailOrCedulaBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Intentar encontrar al usuario por correo electrónico
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # Si no se encuentra por correo, intentar por cédula
            try:
                user = UserModel.objects.get(cedula=username)
            except UserModel.DoesNotExist:
                return None

        # Verificar la contraseña
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None