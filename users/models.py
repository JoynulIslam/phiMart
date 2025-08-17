from django.db import models
from django.contrib.auth.models import AbstractUser
from users.manager import CustomeUserManager

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null= True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)

    USERNAME_FIELD = 'email' #use email instead of username
    REQUIRED_FIELDS = []

    objects = CustomeUserManager()

    def __str__(self):
        return self.email
    