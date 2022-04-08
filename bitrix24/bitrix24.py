import requests

BASE_URL = 'https://b24-p3oh6l.bitrix24.com.br/rest/1/0b9h0i30jp6dzz0w'

def send_notification(bitrix_user_id, message):
    response = requests.get(f'{BASE_URL}/im.notify.json?TO={bitrix_user_id}&MESSAGE={message}&TYPE=SYSTEM')
    return response.status_code == 200
