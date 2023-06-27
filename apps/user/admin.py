from django.contrib import admin
from django.utils.html import format_html

from .forms import CongressistaFormAdmin
from .models import Lote, Categoria, Congressista,Pagamento
from django.shortcuts import render, get_object_or_404
from .forms import LancamentoParcelaForm
from django.db.models import Sum
from django.forms.models import BaseModelForm
from django import forms
from django.forms.models import BaseInlineFormSet

from decimal import Decimal
class LoteAdmin(admin.ModelAdmin):

    list_display = [
        "descricao",
        "valor_unitario",
    ]
    ordering = ["valor_unitario"]

admin.site.register(Lote, LoteAdmin)

class CategoriaAdmin(admin.ModelAdmin):

    search_fields = ['tipo']
    list_display = [
        "tipo",
        "sigla",
    ]
    ordering = ["tipo"]

admin.site.register(Categoria, CategoriaAdmin)

class LancamentoParcelaForm(forms.ModelForm, BaseModelForm):
    class Meta:
        model = Pagamento
        fields = ['congressista', 'valor_parcela','tipo',]

class PagamentoInline(admin.TabularInline):
    model = Pagamento
    form = LancamentoParcelaForm
    extra = 1
    max_num = 5
    can_delete = True


class PagamentoInlineFormSet(BaseInlineFormSet):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-data_pagamento')

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        obj.save()
        return obj

class CongressistaAdmin(admin.ModelAdmin):
    change_form_template = "congressita/change_form_congressista.html"
    list_display = ["nome_completo", "categoria", "ano", "uf", "lote","valor_restante","exibir_status_pagamento"]
    list_filter =["nome_completo", "categoria", "ano", "uf",]
    search_fields = ["nome_completo", "categoria", "ano", "uf", "lote","valor_restante","status_pagamento"]
    list_select_related = ['lote']
    form = CongressistaFormAdmin
    change_list_template = "congressita/change_list_congressitas.html"
    inlines = [PagamentoInline]
    readonly_fields = ['valor_total_parcelas', 'valor_restante']

    def exibir_status_pagamento(self, obj):
        valor_restante = obj.valor_restante() if callable(obj.valor_restante) else obj.valor_restante
        if abs(valor_restante) < 0.01:  # Ajuste a tolerância conforme necessário
            return format_html('<span style="color: green;">Pago</span>')
        else:
            return format_html('<span style="color: red;">Pendente</span>')

    exibir_status_pagamento.short_description = 'Status de Pagamento'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_lote=Sum('lote__valor_unitario'))
        return queryset

    def get_total_lote(self, obj):
        return Congressista.objects.all().aggregate(Sum('lote__valor_unitario'))['lote__valor_unitario__sum']


    get_total_lote.admin_order_field = 'total_lote'
    get_total_lote.short_description = 'Total Lote'

    tabs = ("ContratoPessoa",)
    save_on_top = True

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response
        total_lote = (
                Congressista.objects.all().aggregate(Sum('lote__valor_unitario'))['lote__valor_unitario__sum'] or 0
        )

        response.context_data["total_lote"] = total_lote

        return response

    class Media:
        js = ("admin/js/jquery.mask.min.js", "admin/js/custon.js", "jquery.js","admin/js/desativar_fka_pessoa.js")



admin.site.register(Congressista, CongressistaAdmin)

class PagamentoAdmin(admin.ModelAdmin):

    form = LancamentoParcelaForm
    search_fields = ['tipo']
    list_display = [
        "congressista",
        "data_pagamento",
        "valor_parcela",
        "get_valor_lote",
    ]
    ordering = ["congressista"]

    def get_valor_lote(self, obj):
        return obj.congressista.lote.valor_unitario

    get_valor_lote.short_description = 'Valor do Lote'

admin.site.register(Pagamento, PagamentoAdmin)










