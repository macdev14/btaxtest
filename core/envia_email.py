from threading import Thread

from django.core.mail import send_mail
from django.template.loader import render_to_string
<<<<<<< HEAD
=======
<<<<<<< HEAD
from django.utils.html import strip_tags
=======
>>>>>>> debef6e (ls)
>>>>>>> dfe4662f63c38772a690479088e232040a840204

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
<<<<<<< HEAD
=======
<<<<<<< HEAD

        plain_message = strip_tags(html_message)
        from_email = 'Bitrix24.tax <no-reply@bitrix24.tax>'
        send_mail(
            'Cadastro efetuado com sucesso no Bitrix24.tax',
            plain_message,
            from_email,
=======
>>>>>>> dfe4662f63c38772a690479088e232040a840204
        send_mail(
            'Cadastro efetuado com sucesso no Bitrix24.tax',
            '',
            'Bitrix24.tax <no-reply@bitrix24.tax>',
<<<<<<< HEAD
=======
>>>>>>> debef6e (ls)
>>>>>>> dfe4662f63c38772a690479088e232040a840204
            [self.email,],
            fail_silently=False,
            html_message=html_message,
        )
    