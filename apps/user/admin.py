from django.contrib import admin
from django.utils.html import format_html

from .forms import CongressistaFormAdmin
from .models import Lote, Categoria, Congressista,Pagamento
from django.utils.translation import gettext_lazy as _
from django.db.models import F
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
        fields = ['congressista', 'valor_parcela','tipo',"numero_da_parcela"]

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
    list_display = [
        "nome_completo",
        "categoria",
        "ano",
        "uf",
        "lote",
        "valor_restante",
        "exibir_status_pagamento",
        "proxima_parcela",
        "numero_parcelas",
    ]
    list_filter = [
        "categoria",
        "ano",
        "uf",
        "lote",
        "proxima_parcela",
        "numero_parcelass"]
    list_select_related = ['lote']
    form = CongressistaFormAdmin
    change_list_template = "congressita/change_list_congressitas.html"
    inlines = [PagamentoInline]
    readonly_fields = ['valor_total_parcelas', 'valor_restante']
    list_max_show_all = 20


    def exibir_status_pagamento(self, obj):
        valor_restante = obj.valor_restante() if callable(obj.valor_restante) else obj.valor_restante
        if abs(valor_restante) < 0.01:  # Ajuste a tolerância conforme necessário
            return format_html('<span style="color: green;">Pago</span>')
        else:
            return format_html('<span style="color: red;">Pendente</span>')

    exibir_status_pagamento.short_description = 'Status de Pagamento'

    def get_list_filter(self, request):
        return (StatusPagamentoFilter, 'ano', 'categoria','nome_completo',)

    def get_valor_restante(self, obj):
        return obj.valor_restante

    get_valor_restante.admin_order_field = 'valor_restante'
    get_valor_restante.short_description = 'Valor Restante'

    def status_pagamento(self, obj):
        if obj.valor_restante == 0:
            return _('Pago')
        else:
            return _('Pendente')

    status_pagamento.admin_order_field = 'valor_restante'
    status_pagamento.short_description = _('Status de Pagamento')

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

    def get_total_parcelas(self, obj):
        total_parcelas = Congressista.objects.aggregate(total=Sum('pagamento__valor_parcela'))['total']
        return total_parcelas or 0

    get_total_parcelas.admin_order_field = 'valor_total_parcelas'
    get_total_parcelas.short_description = 'Total Parcelas'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        total_lote = Congressista.objects.aggregate(total_lote=Sum('lote__valor_unitario'))['total_lote'] or 0
        get_total_parcelas = Congressista.objects.aggregate(total_parcelas=Sum('pagamento__valor_parcela'))[
            'total_parcelas']

        response.context_data["total_lote"] = total_lote
        response.context_data["get_total_parcelas"] = get_total_parcelas

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
        "numero_da_parcela",
        "get_valor_lote",
    ]
    ordering = ["congressista"]

    def get_valor_lote(self, obj):
        return obj.congressista.lote.valor_unitario

    get_valor_lote.short_description = 'Valor do Lote'

admin.site.register(Pagamento, PagamentoAdmin)

class StatusPagamentoFilter(admin.SimpleListFilter):
    title = _('Status de Pagamento')
    parameter_name = 'status_pagamento'

    def lookups(self, request, model_admin):
        return (
            ('pendente', _('Pendente')),
            ('pago', _('Pago')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'pendente':
            return queryset.filter(valor_restante__gt=0)
        if self.value() == 'pago':
            return queryset.filter(valor_restante=0)










