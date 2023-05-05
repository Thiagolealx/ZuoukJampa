from django.db import models

class Patrocinador(models.Model):
    nome_empresa = models.CharField(max_length=50, blank=False, null=False)
    nome_contato = models.CharField(max_length=50, blank=False, null=False)
    descricao = models.CharField(max_length=300, blank=True, null=False)
    valor_pt = models.FloatField(blank=True, null=False)
    comprovante = models.FileField(upload_to="", default="")
    ano = models.CharField(max_length=4, blank=False, null=False)



    class Meta:
        verbose_name = "Patrocinador"

    def __str__(self) -> str:
        return self.nome_empresa

class Parceiros(models.Model):
    nome = models.CharField(max_length=50, blank=False, null=False)
    uf = models.CharField(max_length=2)
    descricao = models.CharField(max_length=300, blank=True, null=False)
    valor_pc= models.FloatField(blank=True, null=False)
    comprovante = models.FileField(upload_to="", default="")
    ano = models.CharField(max_length=4, blank=False, null=False)



    class Meta:
        verbose_name = "Parceiros"

    def __str__(self) -> str:
        return self.nome


class Contratos(models.Model):
    nome_empresa = models.CharField(max_length=50, blank=False, null=False)
    nome_contato = models.CharField(max_length=50, blank=False, null=False)
    serviço_prestado = models.CharField(max_length=300,blank=True,null=False)
    valor_ct = models.FloatField(blank=False, null=False)
    comprovante = models.FileField(upload_to= "", default="")
    ano = models.CharField(max_length=4, blank=False, null=False)
    #tem um campo que some os valor do contratos

    class Meta:
        verbose_name = "Contrato"

    def __str__(self) -> str:
        return self.nome_empresa

class Estoque(models.Model):
    nome_produto = models.CharField(max_length=50, blank=False, null=False)
    descricao = models.CharField(max_length=300, blank=True, null=False)
    quantidade = models.IntegerField(blank=False, null=False)
    valor_unitario = models.FloatField(blank=False, null=False)
    valor_total = models.FloatField(blank=False, null=False)



