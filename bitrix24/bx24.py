from subprocess import call
from pybitrix24 import Bitrix24, requester, PBx24ArgumentError
from autenticacao.models import User 
from boletos.models import TemplateBoleto
from mongodb import querys
from core.models import *
from rest_framework.authtoken.models import Token
from urllib.parse import urlparse
from btax.settings import CLIENT_ID, CLIENT_SECRET
class bitrixBtax(Bitrix24):
 
    def __init__(self,token_btax=None, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                 user_id=1,auth_hostname=None, instalation=False, hostname=None):
        """
        Initialize object attributes. Note that the application ID and key
        arguments are not required if webhooks will be called only.
        :raise Bx24ArgumentError: If hostname is not set
        :param hostname: str A root URL without a protocol and an ending slash of
            the Bitrix24 account (e.g. b24-60jyw6.bitrix24.com)
        :param client_id: str Application ID
        :param client_secret: str Application key
        :param user_id: int A numeric ID of the user (used by webhooks)
        :param auth_hostname: string A hostname of an auth server for box versions of Bitrix24
        """
        # if hostname is None and instalation==True:
        #     raise PBx24ArgumentError("The 'hostname' argument is required")
        #token_btax='d60da59ddef765bed8c592b5ee8835d7cdf86a9b'
        self._access_token = None
        self._refresh_token = None
        self.auth_hostname = auth_hostname
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_id = user_id
        self.hostname = hostname
        self.token_btax = token_btax
        
        self.user_conta = Token.objects.get(key=token_btax).user.profile.conta
       
        url_parsed = urlparse(self.user_conta.bitrix_dominio).netloc
        self.hostname = url_parsed if url_parsed else self.user_conta.bitrix_dominio

        self._refresh_token = self.user_conta.refresh_token
        #print('refresh_token', self._refresh_token)
        # if not self._refresh_token and not instalation:
        #     raise PBx24ArgumentError("No refresh token found in db")
        if self._refresh_token: self.update_all()
        
    
    def authorized(self):
        if self._refresh_token: 
            print('refresh token', self._refresh_token)
            return True
        return False

    def call(self, method, params=None):
        self.update_all()
        return super().call(method, params)

    def has_refresh_token(self):
        if self._refresh_token:
            return True
        else:
            return False
    def obtain_refresh_token(self):
        self._refresh_token=self.user_conta.refresh_token
        
    def first_time(self, code):
        self.obtain_tokens(code)
        
    # override
    def _request_tokens(self, query):
        url = self._build_oauth_url('token')
        data = requester.request(url, query=query)
        self._access_token = data.get('access_token')
        self._refresh_token = data.get('refresh_token')
        self._expires_in = data.get('expires_in')
        self.user_id = data.get('user_id')
        self.member_id = data.get('member_id')
        #user = Conta.objects.get(id=self.user_conta.id)
        self.user_conta.refresh_token = self._refresh_token
        self.user_conta.bitrix_user_id = self.user_id
        self.user_conta.save()
        self.update_all()
        return data



    def install_robot(self, account_id=None, token=None, bitrix_userid=None,  domain="dev.btax24.com"):
        
        if not token: token = self.token_btax
        if not bitrix_userid: bitrix_userid=self.user_id
        if not account_id: account_id=self.user_conta.id

        if 'localhost' in domain or '127.0.0.1' in domain: domain="btaxtest.herokuapp.com"
        templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(account_id), 'deletado': False })
        print('USER TOKEN:')
        print(token)
      
        
        
        dict_options = {}
        for id_boleto in templates_boletos:
            dict_options[ str(id_boleto.get('_id'))] =  str(id_boleto.get('descricao'))
       
        handler = "https://{domain}/api/token/redirect/?user_token={token}&bitrix_user={bitrix_user_id}".format(domain=domain,token=token, bitrix_user_id=bitrix_userid)

        #handler = "https://btaxtest.herokuapp.com/api/cobrancas/emitir/"
        print("URL Handler")
        print(handler)

    
        try:
            self.call('bizproc.robot.delete', {'CODE': 'btax' })
        except Exception as e:
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
                        'Default': '{{Valor do Titulo}}'
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
            'NAME': 'Btax',
           
            'PROPERTIES': properties,
            'USE_SUBSCRIPTION': 'Y',     
            'RETURN_PROPERTIES': return_properties

        }

       
        add_robo = self.call('bizproc.robot.add', params)
        print("Robot")
        if 'error' in add_robo: raise Exception(add_robo)
        print(add_robo)
        tst = self.call('bizproc.robot.list')
        print(tst)
        

    #def update_robot(self, token, account_id, bitrix_userid,  domain="dev.btax24.com"):
    def update_robot(self, token=None, account_id=None, bitrix_userid=None,  domain="dev.btax24.com"):       
            if not token: token = self.token_btax
            if not bitrix_userid: bitrix_userid=self.user_id
            if not account_id: account_id=self.user_conta.id
            templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(account_id), 'deletado': False })
            
            #handler = 'https://dev.btax24.com/api/cobrancas/emitir/'
            #localhost
            if 'localhost' in domain or '127.0.0.1' in domain: domain="btaxtest.herokuapp.com"
            handler = "https://{domain}/api/cobrancas/emitir/?user_token={token}".format(domain=domain,token=str(token))
            print("HANDLER: ")
            print(handler)
            
            
            
            dict_options = {}
            for id_boleto in templates_boletos:
                dict_options[ str(id_boleto.get('_id'))] =  str(id_boleto.get('descricao'))
            
            
            self.refresh_tokens()
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
                            'Default': '{{Valor do Titulo}}'
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
                            'Name': 'ID Boleto',
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
                'AUTH_USER_ID': bitrix_userid,
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
            self.refresh_tokens()
            update_robo = self.call('bizproc.robot.update', params)
            print(update_robo)
            if 'error' in update_robo: raise Exception(update_robo['error_description'])
        
            print("Update Robot")

    def update_deal(self, query):
            self.call('crm.deal.update', query)

    def delete_robot(self, code):
            self.call('bizproc.robot.delete', {'CODE': code })

    def update_domain(self, domain):
        self.hostname = domain

    def update_all(self, **kwargs):
        kwargs.update({
            'grant_type':'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self._refresh_token
        })
        
        url = self._build_oauth_url('token')
        data = requester.request(url, query=kwargs)
        print(data)
        print(url)
        self._access_token = data.get('access_token')
        self._refresh_token = data.get('refresh_token')
        self._expires_in = data.get('expires_in')
        self.user_id = data.get('user_id')
        self.member_id = data.get('member_id')
        #print(self.user_conta.refresh_token)
        #print(data.get('refresh_token'))
        self.user_conta.refresh_token =  data.get('refresh_token') if data.get('refresh_token') else self.user_conta.refresh_token

        self.user_conta.save()
        #print(self._refresh_token)
        return data