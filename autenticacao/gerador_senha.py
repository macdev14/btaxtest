from random import choice

def gera_senha(tamanho):
    caracters = '0123456789abcdefghijlmnopqrstuwvxz!@#$%&*()'
    senha = ''
    for char in range(tamanho):
        senha += choice(caracters)
    return  senha
