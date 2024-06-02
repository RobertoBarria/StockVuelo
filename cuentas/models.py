from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, Nombre, Apellido, username, email, password=None, avion=None):
        if not email:
            raise ValueError('El usuario debe tener un email')

        if not username:
            raise ValueError('El usuario debe tener un username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            Nombre=Nombre,
            Apellido=Apellido,
            avion=avion,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Nombre, Apellido, email, username, password, avion=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            Nombre=Nombre,
            Apellido=Apellido,
            avion=avion,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Cuenta(AbstractBaseUser):
    Nombre = models.CharField(max_length=50)
    Apellido = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    avion = models.ForeignKey('aviones.Avion', on_delete=models.SET_NULL, null=True, blank=True)
    

    es_administrador = models.BooleanField(default=False)
    es_tripulante = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'Nombre', 'Apellido']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.Nombre} {self.Apellido}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True