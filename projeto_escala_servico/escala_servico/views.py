from django.shortcuts import render
from datetime import date
from escala_servico.models import Militar, Escala
import calendar
from datetime import date, timedelta
from django.db.models import Q

# Função para deletar a escala do mês anterior e gerar nova
def atualizar_escala():
    # pega a data de hoje
    hoje = date.today()
    # altera o dia data atual para o primeiro dia do mês
    inicio_mes_atual = hoje.replace(day=1)

    # pegar o dia da semana (hoje)
    weekday = date.weekday(hoje)
    print('dia da semana:', weekday)

    # Verificar se existe escala para o mês atual
    escala_mes_atual = Escala.objects.filter(mes_referencia=inicio_mes_atual)

    if not escala_mes_atual.exists():
        # Apagar a escala do mês anterior
        Escala.objects.all().delete()

        # Obter as pessoas e gerar nova escala para o mês
        pessoas = list(Militar.objects.all())
        if len(pessoas) < 5:
            raise ValueError("Número insuficiente de pessoas para preencher a escala.")

        # Preencher escala para cada dia útil do mês atual (segunda a sexta)
        for i in range(5):  # Supondo que serão 5 pessoas na primeira semana
            data_escala = inicio_mes_atual + timedelta(days=i)
            print('data escala: ', data_escala)
            pessoa_escalada = pessoas[i % len(pessoas)]  # Pode ser randomizado
            Escala.objects.create(data=data_escala, pessoa=pessoa_escalada, mes_referencia=inicio_mes_atual)

    return Escala.objects.filter(mes_referencia=inicio_mes_atual)


def escala(request):
    meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    list_mes =[]
    
    # Obter o nome de todos os militares
    # militares = Militar.objects.order_by('-antiguidade')
    # print(militares)
    
    data_hoje = date.today()
    mes_atual = data_hoje.month
    ano_atual = data_hoje.year
    mes = meses_do_ano[mes_atual-1]
    # print(f'mês atual: {mes_atual}, ano atua: {ano_atual}')
    # print(mes)

    cal = calendar.monthcalendar(ano_atual, mes_atual)
    # cal = calendar.monthcalendar(2024, 9)
    # print("calendário:", cal)

    # ligando os dias com os militares
    # i = 0
    # for semana in cal:
    #     for dia in semana:
    #         if i == len(militares):
    #             print(i)
    #             i = 0
    #             Escala.objects.create(data=dia, pessoa=militares[i])
    #             i+=1
    #         elif dia == 0:
    #             pass
    #         else:
    #             print(i)
    #             Escala.objects.create(data=dia, pessoa=militares[i])
    #             i+=1
    # escala_do_mes = Escala.objects.order_by("data")

    context = {
        # 'militar': militares,
        'mes_atual':mes,
        'dias_da_semana': dias_semana,
        "mes": list_mes
    }


    # for semana in cal:
    #     dias_do_mes = zip(dias_semana, semana)
    #     list_mes.append(list(dias_do_mes))


    # dia_servico = 0
    # for semana in list_mes:
    #     # print(f"{semana}")
    #     i = 0
    #     indice_mil = 0
    #     # verificando o último que deu serviço na escala
    #     ultimo_servico = Militar.objects.filter(ultimo_a_dar_servico=True).first()
    #     print(f"Último militar a dar serviço: {ultimo_servico}")

    #     for index,nome in enumerate(militares):
    #         if ultimo_servico == nome:
    #             print(f'nome achado {index}: {nome}')
    #             indice_mil = index + 1
    #             break
    #         else:
    #             print('não achado')

    #     # Distribuindo os militares nos dias
    #     while i < len(semana):
    #         if indice_mil < len(militares):
    #             if "Sábado" in semana[i] or "Domingo" in semana[i]:
    #                 # print(semana[i])
    #                 i+=1
    #             else:
    #                 dia_servico = semana[i] + (militares[indice_mil],)
    #                 # print(dia_servico)
    #                 indice_mil+=1
    #                 i+=1
    #         else: 
    #             indice_mil = 0
        
    #     # Salvando o último militar da semana como o último a dar serviço
    #     ultimo_militar = dia_servico[2]
    #     Militar.objects.filter(ultimo_a_dar_servico=True).update(ultimo_a_dar_servico=False)  # Reseta todos
    #     ultimo_militar.ultimo_a_dar_servico = True  # Marca o novo último militar
    #     ultimo_militar.save()  # Salva a alteração

        # print()
    
    escala = atualizar_escala()
    # print(escala)

    return render(request, 'escalas/escala_do_mes.html', context)