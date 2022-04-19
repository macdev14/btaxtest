from boletos.models import TemplateBoleto
from mongodb import querys
from pybitrix24 import Bitrix24
import requests

BASE_URL = 'https://b24-p3oh6l.bitrix24.com.br/rest/1/0b9h0i30jp6dzz0w'

def send_notification(bitrix_user_id, message):
    response = requests.get(f'{BASE_URL}/im.notify.json?TO={bitrix_user_id}&MESSAGE={message}&TYPE=SYSTEM')
    return response.status_code == 200


''' INSTALAR ROBO  '''


def install_robot(token, account_id, bx24, bitrix_userid,  domain="dev.btax24.com"):
        
        # se for local defina como url remoto

        if 'localhost' in domain or '127.0.0.1' in domain: domain="btaxtest.herokuapp.com"
        
        # obter templates de boleto

        templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(account_id), 'deletado': False })
        print('USER TOKEN:')
        print(token)
       
        
        # adicionar a um dicionario
        dict_options = {}
        for id_boleto in templates_boletos:
            dict_options[ str(id_boleto.get('_id'))] =  str(id_boleto.get('descricao'))
        
      
        # criar url
        handler = "https://{domain}/api/token/redirect/?user_token={token}&bitrix_user={bitrix_user_id}".format(domain=domain,token=token, bitrix_user_id=bitrix_userid)

        #handler = "https://btaxtest.herokuapp.com/api/cobrancas/emitir/"
        print("URL Handler")
        print(handler)

    
        try:
            # deletar robo antigo
            bx24.call('bizproc.robot.delete', {'CODE': 'btax' })
        except Exception as e:
            # mostrar erro
            raise Exception("Invalid tokens while deleting robots")
        
        # definir propriedades
        properties = {
            
                'template_boleto_id': {
                        'Name': 'Template de Boleto Cadastrado',
                        'Type': 'select',
                        'Options': dict_options,
                        'Default': list(dict_options.keys())[0] or ''
                    },

                    'sacado_cpf_cnpj': {
                        'Name': 'CPF ou CNPJ do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{CPF ou CNPJ}}'
                    },

                    'sacado_email': {
                        'Name': 'E-mail do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Endereço de E-mail Sacado}}'
                    },
                    
                    'sacado_endereco_bairro': {
                        'Name': 'Bairro do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Bairro do Sacado}}'
                    },

                    'sacado_endereco_logradouro': {
                        'Name': 'Logradouro do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Logradouro do Endereço do Sacado}}'
                    },

                    'sacado_endereco_numero': {
                        'Name': 'Número do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Numero do Endereço do Sacado}}'
                    },

                    'sacado_endereco_complemento': {
                        'Name': 'Complemento do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Complemento de Endereço do Sacado}}'
                    },

                    'sacado_endereco_cep': {
                        'Name': 'CEP do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{CEP do Endereço do Sacado}}'
                    },

                    'sacado_endereco_cidade': {
                        'Name': 'Cidade do endereço do Sacado',
                        'Type': 'string',
                        #Default': ''
                        'Default': '{{Cidade do Endereço do Sacado}}'
                    },

                    'sacado_endereco_uf': {
                        'Name': 'UF do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{UF do Endereço do Sacado}}'
                    },

                    'sacado_endereco_pais': {
                        'Name': 'País do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Pais do Endereço do Sacado}}'
                    },


                    'sacado_nome': {
                        'Name': 'Nome do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Nome do Sacado}}'
                    },

                    'sacado_telefone': {
                        'Name': 'Telefone do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Telefone do Sacado}}'
                    },

                    'sacado_celular': {
                        'Name': 'Celular do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Celular do Sacado}}'
                    },

                    'titulo_valor': {
                        'Name': 'Valor do título',
                        'Type': 'double',
                        #'Default': ''
                        'Default': '{{Valor}}'
                    },

                    'titulo_numero_documento': {
                        'Name': 'Valor para controle interno',
                        'Description': 'Campo que pode ser informado com um valor para controle interno.',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{ID}}'
                    },

                    'titulo_data_vencimento': {
                        'Name': 'Data de vencimento do título ',
                        'Description': 'Data de vencimento do título no formato dd/mm/aaaa.',
                        'Type': 'date',
                        #'Default': ''
                        'Default': '{{Data de Vencimento do Titulo}}'
                    },    
                
                
                    
            }
        # definir propriedades de retorno
        return_properties = {
                    'id': {
                        'Name': 'ID Boleto',
                        'Type': 'string',
                        'Default': '',
                        'Multiple' : 'N',
                    },
                }
        
       
        print("changed!!")
       
        print(properties['template_boleto_id'])
        params = {

            'CODE': 'btax',
            'HANDLER': str(handler),
            
            'AUTH_USER_ID': bitrix_userid,
            'NAME': 'Btax',
           
            'PROPERTIES': properties,
            'USE_SUBSCRIPTION': 'Y',     
            'RETURN_PROPERTIES': return_properties

        }

        # adicionar o robo
        add_robo = bx24.call('bizproc.robot.add', params)
        print("Robot")
        # verificar se possui erro
        if 'error' in add_robo: raise Exception(add_robo)
        print(add_robo)
        #listar o robo
        tst = bx24.call('bizproc.robot.list')
        print(tst)
        


''' ATUALIZAR ROBO  '''



def update_robot(token, account_id, bx24, bitrix_userid,  domain="dev.btax24.com"):
        # obter templates de boleto
        templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(account_id), 'deletado': False })
        
        ''' criar url '''
        handler = 'https://dev.btax24.com/api/cobrancas/emitir/'
        
        # se localhost definir remoto
        if 'localhost' in domain or '127.0.0.1' in domain: domain="btaxtest.herokuapp.com"
        
        # criar url
        handler = "https://{domain}/api/cobrancas/emitir/?user_token={token}".format(domain=domain,token=str(token))
        print("HANDLER: ")
        print(handler)
       
        # guardar no dicionario os boletos
        dict_options = {}
        for id_boleto in templates_boletos:
            dict_options[ str(id_boleto.get('_id'))] =  str(id_boleto.get('descricao'))
        
        
        #bx24.refresh_tokens()
        
        # definir propriedades

        properties = {
            
                'template_boleto_id': {
                        'Name': 'Template de Boleto Cadastrado',
                        'Type': 'select',
                        'Options': dict_options,
                        'Default': list(dict_options.keys())[0] or ''
                    },

                # 'id_boleto': {
                #         'Name': 'ID do Boleto',
                #         'Type': 'string',
                #         'Default': ''
                #     },

                    'sacado_cpf_cnpj': {
                        'Name': 'CPF ou CNPJ do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{CPF ou CNPJ}}'
                    },

                    'sacado_email': {
                        'Name': 'E-mail do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Endereço de E-mail Sacado}}'
                    },
                    
                    'sacado_endereco_bairro': {
                        'Name': 'Bairro do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Bairro do Sacado}}'
                    },

                    'sacado_endereco_logradouro': {
                        'Name': 'Logradouro do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Logradouro do Endereço do Sacado}}'
                    },

                    'sacado_endereco_numero': {
                        'Name': 'Número do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Numero do Endereço do Sacado}}'
                    },

                    'sacado_endereco_complemento': {
                        'Name': 'Complemento do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Complemento de Endereço do Sacado}}'
                    },

                    'sacado_endereco_cep': {
                        'Name': 'CEP do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{CEP do Endereço do Sacado}}'
                    },

                    'sacado_endereco_cidade': {
                        'Name': 'Cidade do endereço do Sacado',
                        'Type': 'string',
                        #Default': ''
                        'Default': '{{Cidade do Endereço do Sacado}}'
                    },

                    'sacado_endereco_uf': {
                        'Name': 'UF do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{UF do Endereço do Sacado}}'
                    },

                    'sacado_endereco_pais': {
                        'Name': 'País do endereço do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Pais do Endereço do Sacado}}'
                    },


                    'sacado_nome': {
                        'Name': 'Nome do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Nome do Sacado}}'
                    },

                    'sacado_telefone': {
                        'Name': 'Telefone do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Telefone do Sacado}}'
                    },

                    'sacado_celular': {
                        'Name': 'Celular do Sacado',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{Celular do Sacado}}'
                    },

                    'titulo_valor': {
                        'Name': 'Valor do título',
                        'Type': 'double',
                        #'Default': ''
                        'Default': '{{Valor}}'
                    },

                    'titulo_numero_documento': {
                        'Name': 'Valor para controle interno',
                        'Description': 'Campo que pode ser informado com um valor para controle interno.',
                        'Type': 'string',
                        #'Default': ''
                        'Default': '{{ID}}'
                    },

                    'titulo_data_vencimento': {
                        'Name': 'Data de vencimento do título ',
                        'Description': 'Data de vencimento do título no formato dd/mm/aaaa.',
                        'Type': 'date',
                        #'Default': ''
                        'Default': '{{Data de Vencimento do Titulo}}'
                    },    
                
                
                    
            }
        # definir propriedades de retorno
        return_properties = {
                    'id': {
                        'Name': 'ID Boleto',
                        'Type': 'string',
                        'Default': ''
                    },
                }
        
      
        print("changed!!")
        
        print(properties['template_boleto_id'])
        params = {

            'CODE': 'btax',
            'HANDLER': str(handler),
            #'AUTH_USER_ID': 'Bearer '+str(token),
            'AUTH_USER_ID': bitrix_userid,
            'USE_SUBSCRIPTION': 'Y',
            #'NAME': 'Btax',
            #'PROPERTIES': properties
            'FIELDS': {
                 
                    'Name': 'Btax',
                    'Type': 'select',
                    'Options': dict_options,
                    'PROPERTIES': properties,
                    'RETURN_PROPERTIES': return_properties

             },    
            #'RETURN_PROPERTIES': return_properties

        }
        print(token)
        #bx24.refresh_tokens()

        # atualizar o robo

        update_robo = bx24.call('bizproc.robot.update', params)
        print(update_robo)
        # verificar se possui erro
        if 'error' in update_robo: raise Exception(update_robo['error_description'])
      
        print("Update Robot")




'''


        BOLETO
    # 'cobranca_id': {
                        'Name': 'cobranca_id',
                        'Type': 'string',
                        'Default': ''
                    },

                    'boleto_id': {
                        'Name': 'boleto_id',
                        'Type': 'string',
                        'Default': ''
                    },

                    'situacao': {
                        'Name': 'situacao',
                        'Type': 'string',
                        'Default': ''
                    },

                    'boleto_url': {
                        'Name': 'boleto_url',
                        'Type': 'string',
                        'Default': ''
                    },

                    'boleto_linha_digitavel': {
                        'Name': 'boleto_linha_digitavel',
                        'Type': 'string',
                        'Default': ''
                    },

                    'boleto_codigo_barras': {
                        'Name': 'boleto_codigo_barras',
                        'Type': 'string',
                        'Default': ''
                    },




    '''