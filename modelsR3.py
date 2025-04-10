from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _

#Necesario para la creacion de los insumos solo para un administrador
from django.contrib import admin
from .models import User

#Clase crear usuarios y su tipo.
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
    
#Clase de permisos para el usuario
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


#Clase que define solo un Administrador con persmisos Django Admin puede crear insumos
class CustomUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_administrador  # propiedad definida en el modelo

    def has_delete_permission(self, request, obj=None):
        return request.user.is_administrador

admin.site.register(User, CustomUserAdmin)

#Clase para la creación y restricción(solo puede un administrador)
class Insumo(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Solo el administrador puede crear insumos
        if not self.creado_por.is_administrador:
            raise PermissionError("Solo el administrador puede crear insumos.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
#Para la gestion de usuarios, en la vista personalizada(en el caso de que se haga)
#if not request.user.is_administrador:
    #return HttpResponseForbidden("Solo administradores pueden realizar esta acción")


#A continuación las clases para las ventas de productos por vendedores(La Bitácora)

#Clase modelo para productos publicados en la Bitácora
class Producto(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Producto: {self.insumo.nombre}"

#Clase modelo para la venta
class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Verificar que el usuario tenga perfil de vendedor
        if not self.vendedor.is_vendedor:
            raise PermissionError("Solo los usuarios con perfil vendedor pueden registrar ventas.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta de {self.producto} por {self.vendedor.email}"

#Hasta aqui cumpliria, hasta el tercer requerimiento funcinal.