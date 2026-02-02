from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    phone_number = models.IntegerField(unique=True, verbose_name='شماره همراه', null=True, blank=True)
    active_phone_number = models.IntegerField(null=True, blank=True, verbose_name='کد فعالسازی شماره')
    email_active_code = models.CharField(null=True, blank=True, max_length=100, verbose_name='کد فعالسازی ایمیل')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره کاربر')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')

    def str(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

