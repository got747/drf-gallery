from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(verbose_name='Username', max_length=30)
    email = models.EmailField(verbose_name='Email', max_length=100, unique=True)
    is_admin = models.BooleanField(verbose_name='Admin', default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.username
