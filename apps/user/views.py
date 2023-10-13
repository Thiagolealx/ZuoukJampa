sourcefrom django.db.models import Sum
from django.shortcuts import render
from .models import Congressista, Entrada, Saida

def caixa_view(request):
    total_parcelas = Congressista.objects.aggregate(total_parcelas=Sum('get_total_parcelas'))['total_parcelas'] or 0
    total_entrada = Entrada.objects.aggregate(total_entrada=Sum('get_valor_total'))['total_entrada'] or 0
    total_saida = Saida.objects.aggregate(total_saida=Sum('get_valor_total'))['total_saida'] or 0

    valor_total_caixa = total_parcelas + total_entrada - total_saida

    context = {
        'total_parcelas': total_parcelas,
        'total_entrada': total_entrada,
        'total_saida': total_saida,
        'valor_total_caixa': valor_total_caixa,
    }

    return render(request, 'caixa.html', context)

