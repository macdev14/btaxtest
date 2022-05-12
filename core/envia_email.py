from threading import Thread

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.utils.html import strip_tags
from django.core.mail import EmailMessage

from btax.settings import EMAIL_HOST_USER
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

        recipient_list=[self.email]
        plain_message = strip_tags(html_message)
        from_email = 'lauro.pimentel@beytech.com.br'
        email_subject = 'Cadastro efetuado com sucesso no Bitrix24.tax'
        
        msg = EmailMessage(
            email_subject, html_message, EMAIL_HOST_USER,  [self.email])
       
        msg.content_subtype = "html"
        
        msg.send()
       

# def EnviaEmail(email, usuario_id, nome):
#     EnviaEmailThread(email, usuario_id, nome).start()
    

# def EnviaEmail(email, usuario_id, nome):
#     html_message = render_to_string(
#             'core/emails/confirmacao-cadastro-conta.html',
#             {
#                 'nome': nome,
#                 'usuario_id': usuario_id,
#             }
#         )

#     recipient_list=[email]
#     plain_message = strip_tags(html_message)
#     from_email = 'Bitrix24.tax <no-reply@bitrix24.tax>'
#     email_subject = 'Cadastro efetuado com sucesso no Bitrix24.tax'
        
#     mail = EmailMultiAlternatives(
#             email_subject, plain_message, from_email,  [recipient_list])
#     mail.attach_alternative(html_message, "text/html")

#     try:
#         mail.send()
#     except Exception as e:
#         print(e)
#         print(e, flush=True)