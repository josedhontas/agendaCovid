from datetime import datetime
import pytz


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
        horario = "13:00"
    elif idade >= 30 and idade <= 39:
        horario = "14:00"
    elif idade >= 40 and idade <= 49:
        horario = "15:00"
    elif idade >= 50 and idade <= 59:
        horario = "16:00"
    else:
        horario = "17:00"
    
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

def Data(data_objeto):
    data_string_formatada = data_objeto.strftime("%Y-%m-%d")
    return data_string_formatada

def converterData(data_objeto):
    data_string_formatada = data_objeto.strftime("%d/%m/%Y")
    return data_string_formatada

def converterHora(hora_objeto):
    hora_string_formatada = hora_objeto.strftime("%H:%M")
    return hora_string_formatada


def Atrasado(data):
    data_str = data.strftime("%Y-%m-%d %H:%M:%S")

    data_fornecida = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
    fuso_horario_brasileiro = pytz.timezone('America/Sao_Paulo')
    data_fornecida = fuso_horario_brasileiro.localize(data_fornecida)
    data_atual = datetime.now(fuso_horario_brasileiro)

    if data_fornecida < data_atual:
        return True
    else:
        return False
    
def diaSemanaInvalido(data):
    if Atrasado(data):
        return True
    dia_semana = obterDiaSemana(data)
    dias_validos = ["Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]
    if dia_semana not in dias_validos:
        return True
    else:
        return False


    



