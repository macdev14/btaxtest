
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from autenticacao.models import User

class OAuthTokenTestCase(APITestCase):

    def setUp(self):
        User.objects.create(
            email='joao.henrique87@outlook.com',
            password='theo2018'
        )

    def test_obtain_token_oauth(self):
        response = self.client.credentials( 
            username='joao.henrique87@outlook.com',
            password='theo2018'
        )
        print('response:', response)
        self.assertTrue(response)