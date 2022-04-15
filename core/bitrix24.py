from boletos.models import TemplateBoleto
from mongodb import querys





def install_robot(token, account_id, bx24, domain="dev.btax24.com"):
    templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(account_id), 'deletado': False })
    print('USER TOKEN:')
    print(token)
    #def dict_append()
    
    
    dict_options = {}
    for id_boleto in templates_boletos:
        dict_options[ str(id_boleto.get('_id'))] =  str(id_boleto.get('descricao'))
    
    #print("templates boletos")
    #print(dict_options)
    #print("USER DETAILS")
    #print(bx24.call('user.current'))
    #print("User options")
    #print(bx24.call('user.option.get'))
    #remoto heroku:
    # handler = 
    #remoto dev.btax:
    handler = 'https://dev.btax24.com/api/cobrancas/emitir/'
    #localhost
    handler = "https://{domain}/api/cobrancas/emitir/".format(domain=domain)

    #handler = "https://btaxtest.herokuapp.com/api/cobrancas/emitir/"
    #print("URL Handler")
    #print(handler)

 #{"HANDLER_URL": "http://localhost:8000/api/cobrancas/emitir/"}
    bx24.call('bizproc.robot.delete', {'CODE': 'btax' })


    properties = {
           
              'template_boleto_id': {
                    'Name': 'Template de Boleto Cadastrado',
                    'Type': 'select',
                    'Options': dict_options,
                    'Default': ''
                },

                'sacado_cpf_cnpj': {
                    'Name': 'CPF ou CNPJ do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{sacado cpf cnpj}}'
                },

                 'sacado_email': {
                    'Name': 'E-mail do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{sacado email}}'
                },

                 'sacado_endereco_logradouro': {
                    'Name': 'Logradouro do endereço do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{endereço logradouro}}'
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
                    'Default': '{{numero documento}}'
                },

                'titulo_data_vencimento': {
                    'Name': 'Data de vencimento do título ',
                    'Description': 'Data de vencimento do título no formato dd/mm/aaaa.',
                    'Type': 'date',
                    #'Default': ''
                    'Default': '{{data vencimento}}'
                },    
            
              
                
        }

    return_properties = {
                'id': {
                     'Name': 'id',
                     'Type': 'string',
                     'Default': ''
                 },
            }
    
    #properties[0][2] = dict_options
    print("changed!!")
    #print(list(properties))
    #properties[0]['template_boleto_id']['Options'] = dict_options
    print(properties['template_boleto_id'])
    params = {

        'CODE': 'btax',
        'HANDLER': str(handler),
        'AUTH_USER_ID': 'Bearer '+str(token),
        'NAME': 'Btax',
        'PROPERTIES': properties,    
        'RETURN_PROPERTIES': return_properties

    }


    add_robo = bx24.call('bizproc.robot.add', params)
    print("Robot")
    print(add_robo)
    tst = bx24.call('bizproc.robot.list')
    print(tst)
     

def atualizar_robot(token, account_id, bx24, domain="dev.btax24.com"):
    templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(account_id), 'deletado': False })
    
    handler = 'https://dev.btax24.com/api/cobrancas/emitir/'
    #localhost
    handler = "https://{domain}/api/cobrancas/emitir/".format(domain=domain)

    handler = "https://btaxtest.herokuapp.com/api/cobrancas/emitir/"
    #def dict_append()
    
    
    dict_options = {}
    for id_boleto in templates_boletos:
        dict_options[ str(id_boleto.get('_id'))] =  str(id_boleto.get('descricao'))
    
    
    return_properties = {
            'id': {
                     'Name': 'id',
                     'Type': 'string',
                     'Default': ''
                 },
        }

    properties = {
           
              'template_boleto_id': {
                    'Name': 'Template de Boleto Cadastrado',
                    'Type': 'select',
                    'Options': dict_options,
                    'Default': ''
                },

                'sacado_cpf_cnpj': {
                    'Name': 'CPF ou CNPJ do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{sacado cpf cnpj}}'
                },

                 'sacado_email': {
                    'Name': 'E-mail do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{sacado email}}'
                },

                 'sacado_endereco_logradouro': {
                    'Name': 'Logradouro do endereço do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{endereço logradouro}}'
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
                    'Default': '{{numero documento}}'
                },

                'titulo_data_vencimento': {
                    'Name': 'Data de vencimento do título ',
                    'Description': 'Data de vencimento do título no formato dd/mm/aaaa.',
                    'Type': 'date',
                    #'Default': ''
                    'Default': '{{data vencimento}}'
                },    
            
              
                
        }

    params = {

        'CODE': 'btax',
        'HANDLER': str(handler),
        'AUTH_USER_ID': str(token),
        'NAME': 'Btax',
        'PROPERTIES': properties,    
        'RETURN_PROPERTIES': return_properties

    }

    
    
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