from datetime import timezone

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db.models import Sum
from django.shortcuts import render
from decimal import Decimal


from django.db import models

def validate_uf(value):
    if not value.isalpha() or not value.isupper():
        raise ValidationError(
            'A UF deve conter apenas letras, sendo elas Maiúsculas')

#Criação do atributos de Lote, Categoria e User
class Lote(models.Model):
    descricao = models.CharField(max_length=20,blank=False, null=False, validators=[MinLengthValidator(5)])
    valor_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Lote"

    def __str__(self) -> str:
        return self.descricao


class Categoria(models.Model):
    tipo = models.CharField(max_length=20,blank=False, null=False, validators=[MinLengthValidator(5)])
    sigla = models.CharField(max_length=2,blank=False, null=False)

    class Meta:
        verbose_name = "Categoria"

    def __str__(self) -> str:
        return self.tipo


class Congressista(models.Model):

    nome_completo = models.CharField(max_length=50, blank=False,null=False)
    cpf = models.CharField(max_length=11,blank=False,null=False)
    contato = models.IntegerField(blank=True,null=True)
    categoria = models.ForeignKey(Categoria,on_delete=models.DO_NOTHING,null=True)
    lote = models.ForeignKey(Lote,on_delete=models.DO_NOTHING,null=False)
    ano = models.CharField(max_length=4,blank=False,null=False)
    cep = models.CharField("CEP", max_length=9, blank=True, null=True,
                           help_text="Digite um CEP válido para atualizar os campos abaixo.")
    logradouro = models.CharField(
        "Logradouro", max_length=200, blank=True, null=True)
    num_endereco = models.CharField(
        "Número", max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=30, blank=True, null=True)
    bairro = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(
        "Município", max_length=100, blank=True, null=True)
    uf = models.CharField("UF", max_length=2, blank=True,
                          null=True, validators=[validate_uf])
    proxima_parcela = models.DateField(blank=True, null=True)

    numero_parcelass = models.IntegerField(blank=True, null=True)
    total_parcelas = models.FloatField(default=0.0)
    def valor_total_parcelas(self):
        return self.pagamento_set.aggregate(total=Sum('valor_parcela'))['total'] or 0

    @property
    def valor_restante(self):
        valor_total = self.lote.valor_unitario
        valor_parcelas = self.pagamento_set.aggregate(total=Sum('valor_parcela'))['total'] or 0
        return valor_total - valor_parcelas

    def status_pagamento(self):
        if self.valor_restante == 0:
            return 'Pago'
        else:
            return 'Pendente'

    def calcular_proxima_parcela(self):
        if self.pagamento_set.exists():
            data_ultima_parcela = self.pagamento_set.latest('data_pagamento').data_pagamento
            proxima_parcela = data_ultima_parcela + timezone.timedelta(days=30)
        else:
            # Se ainda não houver pagamentos, a próxima parcela será 30 dias a partir da data atual
            proxima_parcela = timezone.now() + timezone.timedelta(days=30)
        return proxima_parcela   


    @property
    def numero_parcelas(self):
        return self.pagamento_set.count()

    class Meta:
        verbose_name = "Congressista"

    def __str__(self) -> str:
        return self.nome_completo



class Pagamento(models.Model):

    TIPO =(
        ('CARTAO', 'Cartão de Credito'),
        ('ESPECIE', 'Espécie'),
        ('PIX', 'Pix'),
    )
    congressista = models.ForeignKey(Congressista, on_delete=models.CASCADE)
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2)
    numero_da_parcela = models.IntegerField(blank=False,null=False)
    tipo =models.CharField("Tipo de Pagamento", max_length=20, choices=TIPO)
    data_pagamento = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"


    def __str__(self) -> str:
        return f"{self.congressista.nome_completo} - {self.data_pagamento}"

class Entrada(models.Model):
    descricao = models.CharField(max_length=100, blank=True, null=True)
    valor_unitario = models.DecimalField(verbose_name= "Valor",max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(blank=False, null=False)
    ano = models.IntegerField(max_length=4, blank=False, null=False)
    nome_empresa = models.CharField(max_length=100)
    comprovante = models.ImageField(upload_to='comprovantes/',blank=True, null=False)
    valor_total_entrada = models.FloatField(blank=True, null=False, editable=False)


    def calcular_valor_total(self):
        if self.valor_unitario is not None and self.quantidade is not None:
            return self.valor_unitario * self.quantidade
        return 0

    def save(self, *args, **kwargs):
        self.valor_total = self.calcular_valor_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao

class Saida(models.Model):
    descricao = models.CharField(max_length=100,blank=True, null=False)
    valor_unitario = models.DecimalField(verbose_name="Valor",max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(blank=False, null=False)
    ano = models.IntegerField(max_length=4, blank=False, null=False)
    nome_empresa = models.CharField(max_length=100,blank=True, null=True)
    comprovante = models.ImageField(upload_to='comprovantes/',blank=True, null=False)
    valor_total_saida = models.FloatField(blank=True, null=False, editable=False)

    def calcular_valor_total(self):
        if self.valor_unitario is not None and self.quantidade is not None:
            return self.valor_unitario * self.quantidade
        return 0

    def save(self, *args, **kwargs):
        self.valor_total = self.calcular_valor_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descricao

class Caixa (models.Model):    

    @property
    def congressitas(self):
        return Pagamento.objects.aggregate(total=Sum('valor_parcela'))['total'] or 0
    
    @property
    def entradas(self):
        return Entrada.objects.all().aggregate(Sum('valor_total_entrada'))['valor_total_entrada__sum']
    
    @property
    def saidas(self):
        return Saida.objects.all().aggregate(Sum('valor_total_saida'))['valor_total_saida__sum']

    @property
    def saldo(self):
        return Decimal(self.congressitas) + Decimal(self.entradas) - Decimal(self.saidas)

    
    def __str__(self):
        return self.congressitas









