from distutils.command.config import config
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from pybitrix24 import Bitrix24

from .settings import CLIENT_ID, CLIENT_SECRET
from .config import bx24
#remoto:



@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    global bx24
    try:
        bx24 = Bitrix24(user.conta.bitrix_dominio, CLIENT_ID, CLIENT_SECRET)
    except Exception as e:
        print(e)
        pass