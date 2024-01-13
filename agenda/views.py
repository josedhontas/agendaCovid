from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as authlogin, logout
from validate_docbr import CPF
from django.db.models import Q
from .models import *
from .manager import *
from agenda.validacoes import *
import xml.etree.ElementTree as ET
from django.contrib.auth.decorators import user_passes_test


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
            messages.error(request, 'Menor de idade')
        elif senha1 != senha2:
            messages.error(request, 'As senhas não coincidem')
        elif teve_covid:
            messages.error(request, 'Histórico recente de covid')
            CustomUser.objects.create_user(nome_completo=nome_completo, cpf=cpf, data_nascimento=data_nascimento, grupos_atendimento=grupo_atendimento, password=senha1)
        elif grupo_atendimento in ["População Privada de Liberdade", "Pessoas com Deficiência Institucionalizadas", "Pessoas ACAMADAS de 80 anos ou mais"]:
            messages.error(request, 'Grupo não atendido')
            CustomUser.objects.create_user(nome_completo=nome_completo, cpf=cpf, data_nascimento=data_nascimento, grupos_atendimento=grupo_atendimento, password=senha1)
        else:
            try:
                CustomUser.objects.create_user(nome_completo=nome_completo, cpf=cpf, data_nascimento=data_nascimento, grupos_atendimento=grupo_atendimento, password=senha1)
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
            if user.is_staff:
                return redirect('telaAdmin')
            else:
                return redirect('pag_inicial')        
        else:
            messages.error(request, 'CPF ou Senha Incorreta!')
    return render(request, "login.html")

def pag_inicial(request):
    if request.user.is_authenticated:
        # dados do usuario aqui
        nome = request.user.nome_completo
        cpf = request.user.cpf
        data_nascimento = Data(request.user.data_nascimento)
        apto_agendamento = request.user.apto_agendamento
        apto_agendamento_str = "Sim" if apto_agendamento else "Não"
        agendamento_usuario = Agendamento.objects.filter(Q(usuario=cpf) & Q(finalizado=False))
        
        if apto_agendamento is False:
            botao = 'Início'
            caminho = "3"

        elif(len(agendamento_usuario) > 0):
            botao = 'Listar agendamento'
            caminho = "1"
        
        else:
            botao = 'Novo agendamento'
            caminho = "2"

        
        context = {
            'cpf' : cpf,
            'nome': nome,
            'data_nascimento': data_nascimento,
            'apto_agendamento': apto_agendamento_str,
            'botao': botao,
            'caminho': caminho
        }
        return render(request, "pag_inicial.html", context)
    return redirect('/')




def visu_agendamento(request):
    if request.user.is_authenticated is False:
        return redirect('/')
    
    if request.user.apto_agendamento == False:
        return redirect('pag_inicial')
    
    if request.user.is_authenticated:
        # dados do usuario aqui
        cpf = request.user.cpf
        apto_agendamento = request.user.apto_agendamento
        apto_agendamento_str = "Sim" if apto_agendamento else "Não"

        #aqui comeca os dados do agendamento e estabelecimento
        agendamento = Agendamento.objects.filter(Q(usuario=cpf) & Q(finalizado=False)).last()
        cnes = agendamento.estabelecimento.cnes

        if cnes is None:
            return redirect('pag_inicial')

        estabelecimento = Estabelecimento.objects.filter(cnes = cnes).first()
        estabelecimento_nome = estabelecimento.nome
        diaSemana = obterDiaSemana(agendamento.data_agendamento)
        data = converterData(agendamento.data_agendamento)
        hora = converterHora(agendamento.data_agendamento)
        atrasado = Atrasado(agendamento.data_agendamento)
        atrasado_str = "Sim" if atrasado else "Não"

        agendamento.atrasado = atrasado
        agendamento.finalizado = atrasado
        agendamento.save()

        
        context = {
            'data' : data,
            'hora': hora,
            'cnes': cnes,
            'diaSemana': diaSemana,
            'estabelecimento': estabelecimento_nome,
            'atrasado': atrasado_str
        }
        return render(request, "visu_agendamento.html", context)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')

def agendamento(request):
    if request.user.is_authenticated is False:
        return redirect('/')
    
    if request.user.apto_agendamento == False:
        return redirect('pag_inicial')
    
    if request.method == 'POST':
        usuario = request.user
        cnes = request.POST.get('cnes')
        estabelecimento = Estabelecimento.objects.get(cnes=cnes)
        dia = request.POST.get('dia')
        horario = request.POST.get('horario')

        data_hora_agendamento = datetime.strptime(f"{dia} {horario}", "%Y-%m-%d %H:%M")
        data_hora_agendamento = timezone.make_aware(data_hora_agendamento, timezone.utc)
        agendamento_usuario = Agendamento.objects.filter(Q(usuario=usuario.cpf) & Q(finalizado=False))

        estabelecimento_cheio = Agendamento.objects.filter(Q(data_agendamento=data_hora_agendamento) & Q(finalizado=False) & Q(estabelecimento=cnes))

        if Atrasado(data_hora_agendamento):
            messages.error(request, 'Data inválida')
        elif len(agendamento_usuario) >= 1:
            messages.error(request, 'Agendamento já feito')
        elif diaSemanaInvalido(data_hora_agendamento):
            messages.error(request, 'Selecione dias entre quarta e sábado')
        elif len(estabelecimento_cheio) >= 5:
            messages.error(request, 'Estabelecimento sem vagas para o horário')
        else:
            agendamento = Agendamento(usuario=usuario, estabelecimento=estabelecimento,  data_agendamento=data_hora_agendamento)
            messages.success(request, 'Agendamento realizado com sucesso!')
            agendamento.save()
            return redirect('visu_agendamento')



    data_nascimento = request.user.data_nascimento
    tree = ET.parse('agenda/dados/estabelecimentos_pr.xml')
    dados_xml = [{'nome': estabelecimento.find('no_fantasia').text, 'cnes': estabelecimento.find('co_cnes').text} for estabelecimento in tree.getroot().findall('.//estabelecimento')]
    context = {'dados_xml': dados_xml}
    horario = regraHorario(str(data_nascimento))
    nome_horario = horario + " horas"
    
    context2 = {
        'horario': horario,
        'nome_horario': nome_horario,
    }

    context = {**context, **context2}

    return render(request, "agendamento.html", context)

from django.shortcuts import render


@user_passes_test(lambda u: u.is_staff)
def telaAdmin(request):

    estabelecimentos = Estabelecimento.objects.all()

    info = [
        {
            'nome': estabelecimento.nome,
            'cnes': estabelecimento.cnes
        }
        for estabelecimento in estabelecimentos
    ]

    dados = {'info': info}


    return render(request, 'telaAdmin.html', context=dados)


@user_passes_test(lambda u: u.is_staff)
def graficoBarra(request):
    estabelecimentos = Estabelecimento.objects.all()

    estabelecimentos = [
        {
            'nome': estabelecimento.nome,
            'agendamentos': len(Agendamento.objects.filter(Q(estabelecimento=estabelecimento.cnes) & Q(finalizado=False)))
        }
        for estabelecimento in estabelecimentos
    ]

    dados = {'estabelecimentos': estabelecimentos}
    return render(request, 'graficoBarra.html', context=dados)

@user_passes_test(lambda u: u.is_staff)
def graficoPizza(request):
    estabelecimentos = Estabelecimento.objects.all()

    estabelecimentos = [
        {
            'nome': estabelecimento.nome,
            'agendamentos': len(Agendamento.objects.filter(Q(estabelecimento=estabelecimento.cnes) & Q(finalizado=False)))
        }
        for estabelecimento in estabelecimentos
    ]

    dados = {'estabelecimentos': estabelecimentos}
    return render(request, 'graficoPizza.html', context=dados)

