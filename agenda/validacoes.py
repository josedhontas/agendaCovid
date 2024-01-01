from datetime import datetime

def validaData(data):
    try:
        data = datetime.date.fromisoformat(data)
    except ValueError or AttributeError:
        return False
    dias_ano = 365.2425
    idade = int((datetime.date.today() - data).days / dias_ano)
    if idade >= 18:
        return True
    else:
        return False

def regraHorario(data_nascimento):
    idade = calcular_idade(data_nascimento)
    horario = None
    if idade >= 18 and idade <= 29:
        horario = "13 horas"
    elif idade >= 30 and idade <= 39:
        horario = "14 horas"
    elif idade >= 40 and idade <= 49:
        horario = "15 horas"
    elif idade >= 50 and idade <= 59:
        horario = "16 horas"
    else:
        horario = "17 horas"
    
    return horario


def calcular_idade(data_nascimento):
    data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d')
    
    data_atual = datetime.now()
    
    diferenca = data_atual - data_nascimento
    
    idade = diferenca.days // 365
    
    return idade

def obterDiaSemana(data):
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    return dias_semana[data.weekday()]

def converterData(data_objeto):
    data_string_formatada = data_objeto.strftime("%Y-%m-%d")
    return data_string_formatada

def converterHora(hora_objeto):
    hora_string_formatada = hora_objeto.strftime("%H:%M")
    return hora_string_formatada
