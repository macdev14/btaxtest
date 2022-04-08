from threading import Thread

from django.core.mail import send_mail
from django.template.loader import render_to_string

class EnviaEmail(Thread):

    def __init__(self, email, usuario_id, nome):
        Thread.__init__(self)
        self.email = email
        self.usuario_id = usuario_id
        self.nome = nome

    def run(self):
        html_message = render_to_string(
            'core/emails/confirmacao-cadastro-conta.html',
            {
                'nome': self.nome,
                'usuario_id': self.usuario_id,
            }
        )
        send_mail(
            'Cadastro efetuado com sucesso no Bitrix24.tax',
            '',
            'Bitrix24.tax <no-reply@bitrix24.tax>',
            [self.email,],
            fail_silently=False,
            html_message=html_message,
        )
    