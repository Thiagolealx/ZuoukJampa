from django.contrib import admin
from .models import Lote, Categoria, Congressista
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import path

class LoteAdmin(admin.ModelAdmin):

    list_display = [
        "descricao",
        "valor",
    ]
    ordering = ["descricao"]

admin.site.register(Lote, LoteAdmin)

class CategoriaAdmin(admin.ModelAdmin):

    search_fields = ['tipo']
    list_display = [
        "tipo",
        "sigla",
    ]
    ordering = ["tipo"]

admin.site.register(Categoria, CategoriaAdmin)

class CongressitaAdmin(admin.ModelAdmin):

    list_display = ["nome_completo", "categoria","lote", "ano","uf",]
    search_fields = ['cep']
    # def save_model(self, request, obj, form, change):
    #     obj.buscar_endereco()

    ordering = ["lote"]

admin.site.register(Congressista, CongressitaAdmin)