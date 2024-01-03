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
    apto_agendamento = models.BooleanField(default= False)
    objects = UserManager()
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = []


class Estabelecimento(models.Model):
    cnes = models.CharField(primary_key = True, max_length=20)
    nome = models.CharField(max_length=100)

class Agendamento(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    data_agendamento = models.DateTimeField()
    finalizado = models.BooleanField(default=False) 


