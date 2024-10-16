from django.shortcuts import render
from escala_servico.models import Militar, Escala
import calendar
from datetime import date, timedelta
from django.db.models import Q

# Função para deletar a escala do mês anterior e gerar nova
def atualizar_escala():
    # pega a data de hoje
    hoje = date.today()
    # hoje.weekday()
    # altera o dia data atual para o primeiro dia do mês
    inicio_mes_atual = hoje.replace(day=1, month=9)

    # pegar o dia da semana (hoje)
    # weekday = date.weekday(hoje)
    # print('dia da semana:', weekday)

    # Verificar se existe escala para o mês atual
    escala_mes_atual = Escala.objects.filter(mes_referencia=inicio_mes_atual)

    if not escala_mes_atual.exists():
        # Apagar a escala do mês anterior
        Escala.objects.all().delete()

        # Obter as pessoas e gerar nova escala para o mês
        militares = list(Militar.objects.order_by('-antiguidade'))
        # if len(pessoas) < 5:
        #     raise ValueError("Número insuficiente de pessoas para preencher a escala.")
        efetivo = len(militares)
        print(efetivo)

        # Preencher escala para cada dia útil do mês atual (segunda a sexta)
        for i in range(efetivo):  # Supondo que serão 5 pessoas na primeira semana
            data_escala = inicio_mes_atual + timedelta(days=i)
            print('data escala: ', data_escala)
            pessoa_escalada = militares[i % len(militares)]  # Pode ser randomizado
            Escala.objects.create(data=data_escala, pessoa=pessoa_escalada, mes_referencia=inicio_mes_atual)

    return Escala.objects.filter(mes_referencia=inicio_mes_atual)

def preencher_escala():
    # esta função vai ficar responsável por preencher todos os dias do mes com os mlitares disponíveis no banco de dados
    ...

def escala(request):
    escala = atualizar_escala()
    meses_do_ano = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    data_hoje = date.today()
    mes_atual = data_hoje.month
    ano_atual = data_hoje.year
    mes = meses_do_ano[mes_atual-1]

    cal = calendar.monthcalendar(ano_atual, mes_atual)
    # cal = calendar.monthcalendar(2024, 9)
    # print("calendário:", cal)

    data = Escala.objects.order_by('data')
    for dia in data:
        if dia.data.day == 1:
            primeiro_dia_da_semana = dia.data.weekday()
            print("primeiro dia da semana:", primeiro_dia_da_semana)
        print(dia.data, dia.pessoa, dia.data.weekday())
    
    list_qtd_quadrados = []
    for i in range(primeiro_dia_da_semana):
        # print('Adicionando um quadrado')
        list_qtd_quadrados.append(0)

    qtd_list = len(list_qtd_quadrados)
    print('tamanho da lista', qtd_list)

    context = {
        'mes_atual':mes,
        'data': data,
        'qtd_quadrados': list_qtd_quadrados,
        'tamanho_lista': qtd_list,
        # "mes": cal,
        'escala': escala
    }

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

    return render(request, 'escalas/escala_do_mes.html', context)