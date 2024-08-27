'''
### código para montar o calendário 
obs: execute este código em outro ambiente ou no terminal
import datetime

for i in range(1, 31, 1): # começa de 1,vai até 30 de 1 passo em 1
    x = datetime.datetime(2024, 4, i)
    print(x.strftime("%A"), i)

'''
from django.shortcuts import render
from datetime import date
import calendar


# Create your views here.
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
        # list_dias.append(zip(dias_semana, semana))
        dias_do_mes = zip(dias_semana, semana)
        list_mes.append(list(dias_do_mes))

    return render(request, 'escalas/escala_do_mes.html', {'mes_atual':mes, 'dias_semana': dias_semana, "mes": list_mes})
