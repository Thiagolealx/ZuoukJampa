from django.contrib import admin
from .models import Contratos, Patrocinador,Parceiros, Estoque

class ContratosAdmin(admin.ModelAdmin):

    list_display = [
        "nome_empresa",
        "valor_ct",
        "nome_contato"
    ]
    ordering = ["nome_empresa"]

admin.site.register(Contratos, ContratosAdmin)

class PatrocinadorsAdmin(admin.ModelAdmin):

    list_display = [
        "nome_empresa",
        "valor_pt",
        "nome_contato"
    ]
    ordering = ["nome_empresa"]

admin.site.register(Patrocinador, PatrocinadorsAdmin)

class ParceirosAdmin(admin.ModelAdmin):

    list_display = [
        "nome",
        "uf",
        "ano"
    ]
    ordering = ["nome"]

admin.site.register(Parceiros, ParceirosAdmin)


class EstoqueAdmin(admin.ModelAdmin):

    list_display = [
        "nome_produto",
        "descricao",
        "quantidade"
    ]
    ordering = ["nome_produto"]

admin.site.register(Estoque, EstoqueAdmin)



