from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as authlogin, logout
from validate_docbr import CPF
from .models import *
from .manager import *
from agenda.validacoes import *
import xml.etree.ElementTree as ET

def cadastro(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        grupo_atendimento = request.POST.get('grupo_atendimento')
        teve_covid = request.POST.get('teve_covid') == 'sim'
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')
        apto_agendamento = True

        _cpf = CPF()
        if not _cpf.validate(cpf):
            messages.error(request, 'CPF Inválido!')
        elif CustomUser.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado')
        elif not validaData(data_nascimento):
            messages.error(request, 'Data inválida')
        elif senha1 != senha2:
            messages.error(request, 'As senhas não coincidem')
        elif teve_covid:
            messages.error(request, 'Histórico recente de covid')
        elif grupo_atendimento in ["População Privada de Liberdade", "Pessoas com Deficiência Institucionalizadas", "Pessoas ACAMADAS de 80 anos ou mais"]:
            messages.error(request, 'Grupo não atendido')
        else:
            try:
                CustomUser.objects.create_user(nome_completo=nome_completo, cpf=cpf, data_nascimento=data_nascimento, grupos_atendimento=grupo_atendimento, apto_agendamento=apto_agendamento, password=senha1)
                messages.success(request, 'Cadastro realizado com sucesso!')
            except:
                messages.error(request, 'Usuário já está cadastrado')

    tree = ET.parse('agenda/dados/grupos_atendimento.xml')
    dados_xml = [grupo.find('nome').text for grupo in tree.getroot().findall('.//grupoatendimento')]

    return render(request, "cadastro.html", {'dados_xml': dados_xml})

def login(request):
    if request.user.is_authenticated:
        return redirect('pag_inicial')
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        user = authenticate(request, cpf=cpf, password=senha)
        if user is not None:
            authlogin(request, user)
            return redirect('pag_inicial')
        else:
            messages.error(request, 'CPF ou Senha Incorreta!')
    return render(request, "login.html")

def pag_inicial(request):
    if request.user.is_authenticated:
        nome = request.user.nome_completo
        cpf = request.user.cpf
        data_nascimento = request.user.data_nascimento
        apto_agendamento = request.user.apto_agendamento

        apto_agendamento_str = "Sim" if apto_agendamento else "Não"

        
        context = {
            'cpf' : str(cpf),
            'nome': str(nome),
            'data_nascimento': str(data_nascimento),
            'apto_agendamento': apto_agendamento_str
        }
        return render(request, "pag_inicial.html", context)
    return redirect('/')

    

def logout_view(request):
    logout(request)
    return redirect('/')

def agendamento(request):
    if request.user.is_authenticated is False:
        return redirect('/')
    
    if request.method == 'POST':
        usuario = request.user
        cnes = request.POST.get('cnes')
        print(cnes)
        estabelecimento = Estabelecimento.objects.get(cnes=cnes)
        dia = request.POST.get('dia')
        print(estabelecimento)
        #hora = request.POST.get('hora')
        agendamento = Agendamento(usuario=usuario, estabelecimento=estabelecimento,  data_agendamento=timezone.now())
        agendamento.save()

    data_nascimento = request.user.data_nascimento
    tree = ET.parse('agenda/dados/estabelecimentos_pr.xml')
    dados_xml = [{'nome': estabelecimento.find('no_fantasia').text, 'cnes': estabelecimento.find('co_cnes').text} for estabelecimento in tree.getroot().findall('.//estabelecimento')]
    context = {'dados_xml': dados_xml}

    print(dados_xml)
    
    context2 = {
        'nome_horario': regraHorario(data_nascimento),
    }

    context = {**context, **context2}

    return render(request, "agendamento.html", context)