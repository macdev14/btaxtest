from django.test import TestCase
import json

from boletos.serializers import CobrancaSerializer
from core.models import Conta

class CobrancaSerializerTestCase(TestCase):

    def setUp(self):
        Conta.objects.create(
            nome='Joao Henrique',
            
        )
    def test_is_valid(self):
        conta = Conta.objects.get(nome='Joao Henrique')
        cobranca = CobrancaSerializer(data={
            'conta':conta,
        })

        self.assertTrue(cobranca.is_valid())