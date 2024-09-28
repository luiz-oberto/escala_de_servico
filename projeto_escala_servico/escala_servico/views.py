from django.shortcuts import render
from datetime import date
from escala_servico.models import Militar 
import calendar


def escala(request):
    meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    list_mes =[]
    militares = Militar.objects.order_by('-antiguidade')
    
    data_hoje = date.today()
    mes_atual = data_hoje.month
    ano_atual = data_hoje.year
    mes = meses_do_ano[mes_atual-1]
    # print(f'mês atual: {mes_atual}, ano atua: {ano_atual}')
    # print(mes)

    cal = calendar.monthcalendar(ano_atual, mes_atual)
    # cal = calendar.monthcalendar(2024, 9)
    # print("calendário:", cal)

    context = {
        'militar': militares,
        'mes_atual':mes,
        'dias_da_semana': dias_semana,
        "mes": list_mes
    }


    for semana in cal:
        dias_do_mes = zip(dias_semana, semana)
        list_mes.append(list(dias_do_mes))


    dia_servico = 0
    for semana in list_mes:
        # print(f"{semana}")
        i = 0
        indice_mil = 0
        # verificando o último que deu serviço na escala
        ultimo_servico = Militar.objects.filter(ultimo_a_dar_servico=True).first()
        print(f"Último militar a dar serviço: {ultimo_servico}")

        for index,nome in enumerate(militares):
            if ultimo_servico == nome:
                print(f'nome achado {index}: {nome}')
                indice_mil = index + 1
                break
            else:
                print('não achado')

        # Distribuindo os militares nos dias
        while i < len(semana):
            if indice_mil < len(militares):
                if "Sábado" in semana[i] or "Domingo" in semana[i]:
                    print(semana[i])
                    i+=1
                else:
                    dia_servico = semana[i] + (militares[indice_mil],)
                    print(dia_servico)
                    indice_mil+=1
                    i+=1
            else: 
                indice_mil = 0
        
        # Salvando o último militar da semana como o último a dar serviço
        ultimo_militar = dia_servico[2]
        Militar.objects.filter(ultimo_a_dar_servico=True).update(ultimo_a_dar_servico=False)  # Reseta todos
        ultimo_militar.ultimo_a_dar_servico = True  # Marca o novo último militar
        ultimo_militar.save()  # Salva a alteração

        print()

    return render(request, 'escalas/escala_do_mes.html', context)