import datetime
from xml.dom import ValidationErr

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
    


def regraHorario(data):
    dias_ano = 365.2425
    idade = int((datetime.date.today() - data).days / dias_ano)
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