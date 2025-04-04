from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):


    #Base para crear usuarios y superusuarios
    def _create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #Usuario Normal
    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    #Superusuario
    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser):

    class Meta:
        db_table = 'users_user'


    email = models.EmailField(unique=True)

    USER_TYPE_CHOICES = (
        (1, 'Administrador'),
        (2, 'Vendedor'),
        (3, 'Promotor'),
    )


    email = models.EmailField(_('email address'), unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def is_administrador(self):
        return self.user_type == 1
    
    @property
    def is_vendedor(self):
        return self.user_type == 2
    
    @property
    def is_promotor(self):
        return self.user_type == 3