import re
from datetime import datetime
class Evento_Validator:
    
    def __init__(self) -> None:
        pass

    def validate(self, request):
        if not request.data['nome']:
            return 'Nome do evento não pode ser vazio', 400
        if not request.data['descricao']:
            return 'Descrição do evento não pode ser vazio',400
        if not request.data['hora']:
            return 'Hora do evento não pode ser vazio',400
        if not request.data['local']:
            return 'Local do evento não pode ser vazio',400
        
        data = request.data['data']
        regex = re.compile(r'^\d{2}/\d{2}/\d{4}$')
        regex_bd = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if regex_bd.match(data):
            data = data[8:] + '/' + data[5:7] + '/' + data[:4]
        if not data:
            return 'Data do evento não pode ser vazio',400
        if not regex.match(data):
            return 'Data do evento deve estar no formato dd/mm/aaaa',400
        
        dia_atual = datetime.now().day
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year
        dia_evento = int(data[:2])
        mes_evento = int(data[3:5])
        ano_evento = int(data[6:])
        if ano_evento < ano_atual:
            return 'Ano do evento não pode ser no passado',400
        elif ano_evento == ano_atual:
            if mes_evento < mes_atual:
                return 'Mês do evento não pode ser no passado',400
            elif mes_evento == mes_atual:
                if dia_evento < dia_atual:
                    return 'Dia do evento não pode ser no passado',400

        return 'Evento criado com sucesso', 200

