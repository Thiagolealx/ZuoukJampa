from datetime import timezone

from django.core.exceptions import ValidationError
from validate_docbr import CPF
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
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE, null=True,default=1)
    lote = models.ForeignKey(Lote,on_delete=models.DO_NOTHING,null=False)
    ano = models.CharField(max_length=4,blank=False,null=False)
    cep = models.CharField("CEP", max_length=9, blank=True, null=True,
                           help_text="Digite um CEP válido para atualizar os campos abaixo.")
    # logradouro = models.CharField(
    #     "Logradouro", max_length=200, blank=True, null=True)
    # num_endereco = models.CharField(
    #     "Número", max_length=10, blank=True, null=True)
    # complemento = models.CharField(max_length=30, blank=True, null=True)
    # bairro = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(
        "Município", max_length=100, blank=True, null=True)
    uf = models.CharField("UF", max_length=2, blank=True,
                          null=True, validators=[validate_uf])
    proxima_parcela = models.DateField(blank=True, null=True)

    # numero_parcelass = models.IntegerField(blank=True, null=True)
    total_parcelas = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Cadastro"
        verbose_name_plural = "Cadastro"
    
#Validação do Cpf:
    def clean(self):
        super().clean()
        if self.cpf:
            cpf = self.cpf.replace(".", "").replace("-", "").strip()
            if not CPF().validate(cpf):
                raise ValidationError('CPF inválido.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Congressista, self).save(*args, **kwargs)
    
# Calculo pra somar as parcelas:
    def valor_total_parcelas(self):
        return self.pagamento_set.aggregate(total=Sum('valor_parcela'))['total'] or 0
    
    def valor_total_categoria_8(self):
        categoria_id =[8,9]
        valor_total = self.pagamento_set.filter(categoria=categoria_id).aggregate(total=Sum('valor_parcela'))['total'] or 0        
        return valor_total
    
    def valor_total_baile(self):
        categoria_id =[2,3]
        valor_total = self.pagamento_set.filter(categoria=categoria_id).aggregate(total=Sum('valor_parcela'))['total'] or 0        
        return valor_total
    
    def valor_total_congresso(self):
        categoria_id =[1,]
        valor_total = self.pagamento_set.filter(categoria=categoria_id).aggregate(total=Sum('valor_parcela'))['total'] or 0        
        return valor_total

    def get_valor_restante(self):
        valor_total = self.lote.valor_unitario
        valor_parcelas = self.pagamento_set.aggregate(total=Sum('valor_parcela'))['total'] or 0
        return valor_total - valor_parcelas

    def status_pagamento(self):
        if self.valor_restante == 0:
            return 'Pago'
        else:
            return 'Pendente'

    def atualizar_proxima_parcela(self):
        print(self.pagamento_set.exists())
        if self.pagamento_set.exists():
            data_ultima_parcela = self.pagamento_set.latest('data_pagamento').data_pagamento
            proxima_parcela = data_ultima_parcela + timezone.timedelta(days=30)
        else:
            proxima_parcela = timezone.now() + timezone.timedelta(days=30)

        self.proxima_parcela = proxima_parcela
        self.save()
   
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
    numero_da_parcela = models.IntegerField(blank=True,null=True)
    tipo =models.CharField("Tipo de Pagamento", max_length=20, choices=TIPO)
    data_pagamento = models.DateField(auto_now_add=True)
    categoria= models.ForeignKey(Categoria,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"


    def __str__(self) -> str:
        return f"{self.congressista.nome_completo} - {self.data_pagamento}"

class Entrada(models.Model):
    """
    Represents an entry in a financial system.

    Fields:
    - descricao: CharField to store the description of the entry.
    - valor_unitario: DecimalField to store the unit price of the entry.
    - quantidade: IntegerField to store the quantity of the entry.
    - ano: IntegerField to store the year of the entry.
    - nome_empresa: CharField to store the name of the company associated with the entry.
    - https://soundcloud.com/i2acoficial/essa-noite-prod-dj-kakah?si=caff1fc402004d739bb0ea09a7be3174&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharingcomprovante: ImageField to store the receipt image of the entry.
    - valor_total_entrada: FloatField to store the calculated total value of the entry. This field is editable=False, meaning it cannot be directly modified by users.
    """

    descricao = models.CharField(max_length=100, blank=True, null=True)
    valor_unitario = models.DecimalField(verbose_name="Valor", max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(blank=False, null=False)
    ano = models.IntegerField(blank=False, null=False)
    nome_empresa = models.CharField(max_length=100)
    comprovante = models.ImageField(upload_to='comprovantes/', blank=True, null=False)
    valor_total_entrada = models.FloatField(blank=True, null=False, editable=False)

    def calcular_valor_total(self):
        """
        Calculates the total value of the entry.

        Returns:
        - The total value of the entry (unit price * quantity) if both unit price and quantity are not None.
        - 0 otherwise.
        """
        if self.valor_unitario is not None and self.quantidade is not None:
            return self.valor_unitario * self.quantidade
        return 0

    def save(self, *args, **kwargs):
        """
        Overrides the default save mehttps://soundcloud.com/i2acoficial/essa-noite-prod-dj-kakah?si=caff1fc402004d739bb0ea09a7be3174&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharingthod to calculate the total value of the entry before saving it to the database.
        """
        self.valor_total_entrada = self.calcular_valor_total()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the entry description.
        """
        return self.descricao

class Saida(models.Model):
    descricao = models.CharField(max_length=100,blank=True, null=False)
    valor_unitario = models.DecimalField(verbose_name="Valor",max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(blank=False, null=False)
    ano = models.IntegerField( blank=False, null=False)
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
    def day_user(self):
        categoria_id = [8,9]  
        return self.pagamento_set.filter(categoria=categoria_id).aggregate(total=Sum('valor_parcela'))['total'] or 0 @property
    @property
    def baile(self):
        categoria_id = [2,3]  
        return self.pagamento_set.filter(categoria=categoria_id).aggregate(total=Sum('valor_parcela'))['total'] or 0 
    @property
    def congressista(self):
        categoria_id = [1,]  
        return self.pagamento_set.filter(categoria=categoria_id).aggregate(total=Sum('valor_parcela'))['total'] or 0 
    
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









