from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth import *
from .manager import *
from validate_docbr import CPF
from agenda.validacoes import validaData
from django.contrib.auth import login as authlogin, logout
import datetime
from django.utils import timezone
from django.db.models import Count, Max, Min, Sum
from time import time
import xml.etree.ElementTree as ET
import calendar


def cadastro(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        print(nome_completo)
        cpf = request.POST.get('cpf')
        print(cpf)
        data_nascimento = request.POST.get('data_nascimento')
        print(data_nascimento)
        grupo_atendimento = request.POST.get('grupo_atendimento')
        print(grupo_atendimento)
        teve_covid = request.POST.get('teve_covid') == 'sim'
        print(teve_covid)
        senha1 = request.POST.get('senha1')
        print(senha1)
        senha2 = request.POST.get('senha2')

        salvar = True
        _cpf = CPF()
        '''if _cpf.validate(cpf) == False:
            messages.error(request, 'CPF Inválido!')
            salvar = False'''
        usuario = CustomUser.objects.filter(cpf = cpf)

        if salvar == True:
            CustomUser.objects.create_user(nome_completo=nome_completo, cpf=cpf, data_nascimento= data_nascimento, grupos_atendimento = grupo_atendimento, teve_covid = teve_covid, password=senha1) 
            messages.success(request, 'Cadastro realizado com sucesso!')
            
        ''' except:
                messages.error(
                    request, 'Usuario já está cadastrado')
                salvar = False'''
    
    tree = ET.parse('agenda/dados/grupos_atendimento.xml')
    root = tree.getroot()

    # Extrai dados do XML
    dados_xml = []
    for grupo in root.findall('.//grupoatendimento'):
        nome = grupo.find('nome').text
        #print(nome)
        dados_xml.append(nome)
    
    

    return render(request, "cadastro.html", {'dados_xml': dados_xml})


def login(request):
    if request.user.is_authenticated == True:
        return redirect('pag-inicial')
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        user = authenticate(request, cpf=cpf, password=senha)
        if user is not None:
            authlogin(request,user)
            return redirect('lista_usuarios')
        else:
            messages.error(request, 'CPF ou Senha Incorreta!')
    return render(request, "login.html")


def lista_usuarios(request):
    # se usuario esta autenticado libere
    if request.user.is_authenticated == True:
        usuarios = CustomUser.objects.all()
        return render(request, "lista_usuarios.html", {'usuarios': usuarios})