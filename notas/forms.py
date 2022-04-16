from django import forms

class ConsultaNotaForm(forms.Form):

    nota_id = forms.CharField(
        label='ID da Nota',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )