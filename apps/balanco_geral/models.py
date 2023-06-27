from django.db import models
from apps.user.models import Congressista

class Entradas(models.Model):

    nome_empresa = models.CharField(max_length=50, blank=True, null=True)
    descricao = models.CharField(max_length=300, blank=True, null=False)
    valor_ct =  models.DecimalField(verbose_name="Valor da Doação" ,max_digits=8, decimal_places=2)
    comprovante =  models.FileField(upload_to= "", default="",blank=True,null=False)
    ano = models.CharField(max_length=4, blank=False, null=False)

    class Meta:
        verbose_name = "Entradas"

    def __str__(self) -> str:
        return self.nome_empresa


class Saidas(models.Model):
    nome_produto = models.CharField(max_length=50, blank=False, null=False)
    descricao = models.CharField(max_length=300, blank=True, null=False)
    quantidade = models.IntegerField(blank=False, null=False)
    valor_unitario =  models.DecimalField(max_digits=8, decimal_places=2)
    valor_total = models.FloatField(blank=True, null=False, editable=False)

    class Meta:
        verbose_name = "Saidas"

    def __str__(self) -> str:
        return self.nome_produto




