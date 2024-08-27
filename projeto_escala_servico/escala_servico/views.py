from django.shortcuts import render
from datetime import date
import calendar


def escala(request):
    meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    list_mes =[]
    
    data_hoje = date.today()
    mes_atual = data_hoje.month
    ano_atual = data_hoje.year
    mes = meses_do_ano[mes_atual-1]
    print(f'mês atual: {mes_atual}, ano atua: {ano_atual}')
    print(mes)

    cal = calendar.monthcalendar(ano_atual, mes_atual)



    for semana in cal:
        dias_do_mes = zip(dias_semana, semana)
        list_mes.append(list(dias_do_mes))

    return render(request, 'escalas/escala_do_mes.html', {'mes_atual':mes, 'dias_semana': dias_semana, "mes": list_mes})
