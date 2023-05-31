from django.contrib import admin
from .models import Contratos, Patrocinador,Parceiros, Estoque
from django.db.models import Sum

class ContratosAdmin(admin.ModelAdmin):

    list_display = ["nome_empresa", "nome_contato", "valor_ct"]
    ordering = ["nome_empresa"]
    change_list_template = "balanco/change_list_contrato.html"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_contrato=Sum('valor_ct'))
        return queryset

    def get_total_contrato(self, obj):
        return Contratos.objects.all().aggregate(Sum('valor_ct'))['valor_ct__sum']

    get_total_contrato.admin_order_field = 'total_contrato'
    get_total_contrato.short_description = 'Total Contrato'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response
        total_contrato = (
                Contratos.objects.all().aggregate(Sum('valor_ct'))['valor_ct__sum']
        )

        response.context_data["total_contrato"] = total_contrato

        return response

    class Media:
        js = ("admin/js/jquery.mask.min.js", "admin/js/custon.js", "jquery.js", "admin/js/desativar_fka_pessoa.js")


admin.site.register(Contratos, ContratosAdmin)

class PatrocinadorsAdmin(admin.ModelAdmin):

    list_display = ["nome_empresa","valor_pt","nome_contato"]
    ordering = ["nome_empresa"]
    change_list_template = "balanco/change_list_patrocinio.html"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_patrocinador=Sum('valor_pt'))
        return queryset

    def get_total_patrocinador(self, obj):
        return Patrocinador.objects.all().aggregate(Sum('valor_pt'))['valor_pt__sum']

    get_total_patrocinador.admin_order_field = 'total_patrocinador'
    get_total_patrocinador.short_description = 'Total Patrocinador'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response
        total_patrocinador = (
                Patrocinador.objects.all().aggregate(Sum('valor_pt'))['valor_pt__sum']
        )

        response.context_data["total_patrocinador"] = total_patrocinador

        return response

    class Media:
        js = ("admin/js/jquery.mask.min.js", "admin/js/custon.js", "jquery.js", "admin/js/desativar_fka_pessoa.js")


admin.site.register(Patrocinador, PatrocinadorsAdmin)

class ParceirosAdmin(admin.ModelAdmin):

    list_display = ["nome","uf","ano", "valor_pc",]
    ordering = ["nome"]
    change_list_template = "balanco/change_list_parceiros.html"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_parceiros=Sum('valor_pc'))
        return queryset

    def get_total_parceiros(self, obj):
        return Parceiros.objects.all().aggregate(Sum('valor_pc'))['valor_pc__sum']

    get_total_parceiros.admin_order_field = 'total_parceiros'
    get_total_parceiros.short_description = 'Total Parceiros'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response
        total_parceiros = (
                Parceiros.objects.all().aggregate(Sum('valor_pc'))['valor_pc__sum']
        )

        response.context_data["total_parceiros"] = total_parceiros

        return response

    class Media:
        js = ("admin/js/jquery.mask.min.js", "admin/js/custon.js", "jquery.js", "admin/js/desativar_fka_pessoa.js")

admin.site.register(Parceiros, ParceirosAdmin)


class EstoqueAdmin(admin.ModelAdmin):

    list_display = [
        "nome_produto",
        "descricao",
        "quantidade",
        "valor_unitario",
        "valor_total",
    ]
    ordering = ["nome_produto"]
    change_list_template = "balanco/change_list_estoque.html"

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

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response
        total_saidas_estoque = (
            Estoque.objects.all().aggregate(Sum('valor_total'))['valor_total__sum']
        )

        response.context_data["total_saidas_estoque"] = total_saidas_estoque

        return response

    class Media:
        js = ("admin/js/jquery.mask.min.js", "admin/js/custon.js", "jquery.js", "admin/js/desativar_fka_pessoa.js")



admin.site.register(Estoque, EstoqueAdmin)



