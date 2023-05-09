from django.contrib import admin
from .models import Contratos, Patrocinador,Parceiros, Estoque
from django.db.models import Sum

class ContratosAdmin(admin.ModelAdmin):

    list_display = [
        "nome_empresa",
        "nome_contato",
        "valor_ct",
        "get_total_contrato"
    ]
    ordering = ["nome_empresa"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_contrato=Sum('valor_ct'))
        return queryset

    def get_total_contrato(self, obj):
        return Contratos.objects.all().aggregate(Sum('valor_ct'))['valor_ct__sum']

    get_total_contrato.admin_order_field = 'total_contrato'
    get_total_contrato.short_description = 'Total Contrato'


admin.site.register(Contratos, ContratosAdmin)

class PatrocinadorsAdmin(admin.ModelAdmin):

    list_display = [
        "nome_empresa",
        "valor_pt",
        "nome_contato",
        "get_total_patrocinador"
    ]
    ordering = ["nome_empresa"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_patrocinador=Sum('valor_pt'))
        return queryset

    def get_total_patrocinador(self, obj):
        return Patrocinador.objects.all().aggregate(Sum('valor_pt'))['valor_pt__sum']

    get_total_patrocinador.admin_order_field = 'total_patrocinador'
    get_total_patrocinador.short_description = 'Total Patrocinador'


admin.site.register(Patrocinador, PatrocinadorsAdmin)

class ParceirosAdmin(admin.ModelAdmin):

    list_display = [
        "nome",
        "uf",
        "ano",
        "valor_pc",
        "get_total_parceiros"
    ]
    ordering = ["nome"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_parceiros=Sum('valor_pc'))
        return queryset

    def get_total_parceiros(self, obj):
        return Parceiros.objects.all().aggregate(Sum('valor_pc'))['valor_pc__sum']

    get_total_parceiros.admin_order_field = 'total_parceiros'
    get_total_parceiros.short_description = 'Total Parceiros'

admin.site.register(Parceiros, ParceirosAdmin)


class EstoqueAdmin(admin.ModelAdmin):

    list_display = [
        "nome_produto",
        "descricao",
        "quantidade",
        "valor_unitario",
        "valor_total",
        "get_total_saidas_estoque"
    ]
    ordering = ["nome_produto"]

    def save_model(self, request, obj, form, change):
        obj.valor_total = obj.quantidade * obj.valor_unitario
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_saidas_estoque=Sum('valor_total'))
        return queryset

    def get_total_saidas_estoque(self, obj):
        return Estoque.objects.all().aggregate(Sum('valor_total'))['valor_total__sum']

    get_total_saidas_estoque.admin_order_field = 'total_saidas_estoque'
    get_total_saidas_estoque.short_description = 'Total Parceiros'



admin.site.register(Estoque, EstoqueAdmin)



