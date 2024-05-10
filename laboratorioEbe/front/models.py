from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nombre, password=None):
        if not email:
            raise ValueError('Los usuarios deben tener una dirección de email')
        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None):
        user = self.create_user(
            email,
            password=password,
            nombre=nombre,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

class Perfil(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    preferencias = models.TextField()

class Escenario(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

class Simulacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    escenario = models.ForeignKey(Escenario, on_delete=models.CASCADE)
    es_compatible_ar = models.BooleanField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Reporte(models.Model):
    simulacion = models.ForeignKey(Simulacion, on_delete=models.CASCADE)
    contenido = models.TextField()

class Anotacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    simulacion = models.ForeignKey(Simulacion, on_delete=models.CASCADE)
    contenido = models.TextField()

class ControlParental(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    configuracion = models.TextField()

class Soporte(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    consulta = models.TextField()

class Tutorial(models.Model):
    nombre = models.CharField(max_length=255)
    contenido = models.TextField()

class RecursoEducativo(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
