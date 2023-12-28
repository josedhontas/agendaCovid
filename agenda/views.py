from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser, Subforum, Categoria, Topico, Resposta, VinculoSubforum
from django.contrib.auth import *
#from avasus.validacoes import validaData (insira a biblioteca para validar a data )
from validate_docbr import CPF
from agenda.validacoes import validaData
from django.contrib.auth import login as authlogin, logout
import datetime
from django.utils import timezone
from django.db.models import Count, Max, Min, Sum
from time import time
import calendar


def cadastro(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        grupo_atendimento = request.POST.get('grupo_atendimento')
        teve_covid = request.POST.get('teve_covid')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')

        salvar = True
        _cpf = CPF()
        if _cpf.validdate(cpf) == False:
            messages.error(request, 'CPF Inválido!')
            salvar = False
        usuario = CustomUser.objects.filter(cpf = cpf)

        if salvar and True:
            try:
                CustomUser.objects.create_user(nome_completo=nome_completo, cpf=cpf, data_nascimento= data_nascimento, grupo_atendimento = grupo_atendimento, teve_covid = teve_covid, password=senha1)
                messages.success(
                    request, 'Cadastro realizado com sucesso!')
            except:
                messages.error(
                    request, 'Usuario já está cadastrado')
                salvar = False