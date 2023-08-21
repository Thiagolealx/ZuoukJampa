from django import forms
from django.core.validators import RegexValidator
from django.forms import TextInput

from .models import Aluno
class AlunoFormAdmin(forms.ModelForm):
    model = Aluno
    fields = ("__all__")
    widgets = {
        "logradouro": TextInput(attrs={"readonly": "readonly", "style": "width: 270px; background: #f0f0f0;"}),
        "bairro": TextInput(attrs={"readonly": "readonly", "style": "width: 270px; background: #f0f0f0;"}),
        "cidade": TextInput(attrs={"readonly": "readonly", "style": "width: 270px; background: #f0f0f0;"}),
        "uf": TextInput(attrs={"readonly": "readonly", "style": "width: 270px; background: #f0f0f0;"})
    }

    def __init__(self, *args, **kwargs):
        super(AlunoFormAdmin, self).__init__(*args, **kwargs)
        self.fields['cep'].widget.attrs['class'] = 'mask-cep'



    cep = forms.CharField(max_length=9, label='CEP', required=False, validators=[
        RegexValidator(
            regex='^\d{5}-\d{3}$',
            message='CEP com formato inválido.',
            code='invalid_cep'
        )
    ])


from django import forms

class LancamentoParcelaForm(forms.Form):
    nome_ou_cpf = forms.CharField(label="Nome ou CPF", max_length=50)
    valor_parcela = forms.DecimalField(label="Valor da Parcela")
