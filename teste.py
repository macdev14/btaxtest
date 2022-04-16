from plugnotas import plugnotas

nota = [
    {
        "idIntegracao": "XXJHAXYY999",
        "prestador": {
            "cpfCnpj": "08187168000160"
        },
        "tomador": {
            "cpfCnpj": "99999999999999",
            "razaoSocial": "Empresa de Teste LTDA",
            "inscricaoMunicipal": "8214100099",
            "email": "teste@plugnotas.com.br",
            "endereco": {
                "descricaoCidade": "Maringa",
                "cep": "87020100",
                "tipoLogradouro": "Rua",
                "logradouro": "Barao do rio branco",
                "tipoBairro": "Centro",
                "codigoCidade": "4115200",
                "complemento": "sala 01",
                "estado": "PR",
                "numero": "1001",
                "bairro": "Centro"
            }
        },
        "servico": [
            {
                "codigo": "14.10",
                "codigoTributacao": "14.10",
                "discriminacao": "Descrição dos serviços prestados, utilize | para quebra de linha na impressão.",
                "cnae": "7490104",
                "iss": {
                    "tipoTributacao": 7,
                    "exigibilidade": 1,
                    "aliquota": 3
                },
                "valor": {
                    "servico": 1,
                    "descontoCondicionado": 0,
                    "descontoIncondicionado": 0
                }
            }
        ]
    }
]
retorno = plugnotas.emitir_nota(nota)
print(retorno)