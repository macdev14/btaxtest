class Bitrix_btax:
    client_secret_local= "QLwJT6k15YjxJX085UWCOFaqrs4JrQaNKnhhmtu3M3Djg2klcy"
    client_id_local = "local.625425573ccf01.19175085"

# remoto:
    client_id = "local.62542020d85557.44615100"

    client_secret = "8MlsoRMTipPgHzU5ejSfGC6WZWxGm8Cik7nSHaBsLL1V5syQ2r"
    
    domain = 'beytrix.bitrix24.com.br'
    def __init__(self,token, account_id, code, domain="dev.btax24.com"):
        
        #self.request = request
        self.code = code
        self.token = token
        self.account_id = account_id
        self.bx24 = Bitrix24(self.domain, self.client_id, self.client_secret)
        self.bx24.obtain_tokens(self.code)
        schedule.every(1).minutes.do(self.bx24.refresh_tokens)

    def install_robot(self):
        templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(self.account_id), 'deletado': False })
        print('USER TOKEN:')
        print(self.token)
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
        #handler = 'https://dev.btax24.com/token/redirect/'
        #localhost
        handler = "https://{domain}/api/token/redirect/?user_token={token}&bitrix_user={bitrix_user_id}".format(domain=self.domain,token=self.token, bitrix_user_id=self.bitrix_userid)

        #handler = "https://btaxtest.herokuapp.com/api/cobrancas/emitir/"
        print("URL Handler")
        print(handler)

    #{"HANDLER_URL": "http://localhost:8000/api/cobrancas/emitir/"}
        try:
            self.bx24.call('bizproc.robot.delete', {'CODE': 'btax' })
        except Error as e:
            raise Exception("Invalid tokens while deleting robots")

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
            #'AUTH_USER_ID': 'Bearer '+str(token),
            'AUTH_USER_ID': self.bitrix_userid,
            'NAME': 'Btax',
            'PROPERTIES': properties,    
            'RETURN_PROPERTIES': return_properties

        }

        try:
            add_robo = self.bx24.call('bizproc.robot.add', params)
            print("Robot")
            print(add_robo)
            tst = self.bx24.call('bizproc.robot.list')
            print(tst)
        except:
            raise Exception("Invalid tokens")

    def update_robot(self):
        templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(self.account_id), 'deletado': False })
        
        handler = 'https://dev.btax24.com/api/cobrancas/emitir/'
        #localhost
        handler = "https://{domain}/api/cobrancas/emitir/?user_token={token}".format(domain=self.domain,token=str(self.token))
        print("HANDLER: ")
        print(handler)
        #handler = "https://btaxtest.herokuapp.com/api/cobrancas/emitir/"
        #def dict_append()
        
        
        dict_options = {}
        for id_boleto in templates_boletos:
            dict_options[ str(id_boleto.get('_id'))] =  str(id_boleto.get('descricao'))
        
        
        
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
            #'AUTH_USER_ID': 'Bearer '+str(token),
            'AUTH_USER_ID': self.bitrix_userid,
            'NAME': 'Btax',
            'PROPERTIES': properties,    
            'RETURN_PROPERTIES': return_properties

        }
        try:
            update_robo = self.bx24.call('bizproc.robot.update', params)
            print(update_robo)
            print("Update Robot")
        except:
            raise Exception("Invalid tokens while updating robots")
   