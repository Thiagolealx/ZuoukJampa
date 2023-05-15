from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


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
    email = models.CharField(max_length=30,blank=False, null=False, validators=[MinLengthValidator(5)])
    cpf = models.CharField(max_length=11,blank=False,null=False)
    contato = models.IntegerField(blank=False,null=False)
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

    class Meta:
        verbose_name = "Congressista"

    def __str__(self) -> str:
        return self.nome_completo


