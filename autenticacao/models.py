import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token

from datetime import datetime

class UserManager(BaseUserManager):
	""" Define o model manager para o modelo User sem o campo username """

	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		# Cria e salva um User com um email e senha 
		if not email:
			raise ValueError('Um e-mail deve ser setado.')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		Token.objects.create(user=user)
		return user

	def create_user(self, email, password=None, **extra_fields):
		# Cria e salva um usuario normal usando email e senha
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_user_for_customer(self, email, password=None, **extra_fields):
		# Cria e salva um usuario normal usando email e senha
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		extra_fields.setdefault('is_first_login', True)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		# Cria e salva um superuser usando email e senha
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser deve ter setado is_staff=True')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser deve ter setado is_superuser=True')

		return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
	""" User model """
	id = models.UUIDField(
        'Id',
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
	is_first_login = models.BooleanField(
		'first login?',
		default=False,
	)
	username = None
	email = models.EmailField('E-mail', unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	@property
	def get_token(self):
		return Token.objects.filter(user=self).first()

class HistoricoLogin(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)

	data_hora = models.DateTimeField(
		auto_now_add=True
	)
	
	ip = models.GenericIPAddressField(null=True, blank=True)