# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate

from .models import User

class LoginForm(forms.Form):
	email = forms.EmailField(
		label='E-mail',
		max_length=150,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'E-mail',
				'autofocus': ''
			}
		)
	)

	password = forms.CharField(
		label='Senha',
		max_length=30,
		widget=forms.PasswordInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Senha'
			}
		)
	)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not User.objects.filter(email=email):
			raise forms.ValidationError('E-mail não encontrado.')
		return email

	def clean_password(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		if not authenticate(email=email, password=password):
			raise forms.ValidationError(u'Senha incorreta.')
		return password

	def save(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		return authenticate(email=email, password=password)

class UserFirstLoginForm(forms.Form):
	
	password1 = forms.CharField(
		label='Nova Senha',
		max_length=20,
		min_length=6,
		widget=forms.PasswordInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Nova senha',
			}
		)
	)

	password2 = forms.CharField(
		label='Repita a Senha',
		max_length=20,
		min_length=6,
		widget=forms.PasswordInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Repita a senha',
			}
		)
	)

	def clean(self):
		cleaned_data = super().clean()

		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')

		if password1 != password2:
			raise forms.ValidationError('As senhas devem ser iguais.')
		
		return cleaned_data