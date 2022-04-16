import requests, json

API_KEY = '2da392a6-79d2-4304-a8b7-959572c7e44d'
BASE_URL = 'https://api.sandbox.plugnotas.com.br'

headers = {
    'X-API-KEY': API_KEY,
}
def consultar_nota(id_nota):
    response = requests.get(f'{BASE_URL}/nfse/{id_nota}', headers=headers)
    return response.json()

def emitir_nota(nota):
    response = requests.post(f'{BASE_URL}/nfse', json=nota, headers=headers)
    return response.json()