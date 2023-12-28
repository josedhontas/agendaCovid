from django.db import models

from django.db import models
from .manager import *
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.utils import timezone

class CustomUser(AbstractUser):
    username = None
    nome_completo = models.CharField(max_length=60, default=' ')
    cpf = models.CharField(primary_key = True, max_length=11)
    data_nascimento = models.DateField(default=timezone.now)
    grupos_atendimento = models.CharField(max_length=100, blank=True, null=True)
    teve_covid = models.BooleanField(default= False)
    objects = UserManager()
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = []