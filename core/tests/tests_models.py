from django.test import TestCase

from ..models import Conta

class ContaTestCase(TestCase):

    def setUp(self):
        self.conta = Conta.objects.create(
            # nome='Joao Henrique',
        )

    def test_create(self):
        print(self.conta)
        self.assertIsInstance(self.conta, Conta)