class ServicoMongo:
    
    def __init__(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs.get(k, ''))

    def dict_to_mongo(self):
        servico_dict = {
            "codigo": self.codigo,
            "idIntegracao": self.id_integracao,
            "discriminacao": self.discriminacao,
            "codigoTributacao": self.codigo_tributacao,
            "cnae": self.cnae,
            "codigoCidadeIncidencia": self.codigo_cidade_incidencia,
            "descricaoCidadeIncidencia": self.descricao_cidade_incidencia,
            "unidade": self.unidade,
            "quantidade": self.quantidade,
            "iss": {
                "tipoTributacao": self.iss_tipo_tributacao,
                "exigibilidade": self.iss_exigibilidade,
                "retido": self.iss_retido,
                "aliquota": self.iss_aliquota,
                "valor": self.iss_valor,
                "valorRetido": self.iss_valor_retido,
                "processoSuspensao": self.iss_processo_suspensao,
            },
            "obra": {
                "art": self.obra_art,
                "codigo": self.obra_codigo,
                "cei": self.obra_cei,
            },
            "valor": {
                "servico": self.valor_servico,
                "baseCalculo": self.valor_base_calculo,
                "deducoes": self.valor_deducoes,
                "descontoCondicionado": self.valor_desconto_condicionado,
                "descontoIncondicionado": self.valor_desconto_incondicionado,
                "liquido": self.valor_liquido,
                "unitario": self.valor_unitario,
                "valorAproximadoTributos": self.valor_aproximado_tributos,
            },
            "deducao": {
                "tipo": self.deducao_tipo,
                "descricao": self.deducao_descricao,
            },
            "retencao": {
                "pis": {
                    "baseCalculo": self.retencao_pis_base_calculo,
                    "aliquota": self.retencao_pis_aliquota,
                    "valor": self.retencao_pis_valor,
                    "cst": self.retencao_pis_cst,
                },
                "cofins": {
                    "baseCalculo": self.retencao_cofins_base_calculo,
                    "aliquota": self.retencao_cofins_aliquota,
                    "valor": self.retencao_cofins_valor,
                    "cst": self.retencao_cofins_cst,
                },
                "csll": {
                    "aliquota": self.retencao_csll_aliquota,
                    "valor": self.retencao_csll_valor,
                },
                "inss": {
                    "aliquota": self.retencao_inss_aliquota,
                    "valor": self.retencao_inss_valor,
                },
                "irrf": {
                    "aliquota": self.retencao_irrf_aliquota,
                    "valor": self.retencao_irrf_valor,
                },
                "outrasRetencoes": self.retencao_outras_retencoes,
                "cpp": {
                    "aliquota": self.retencao_cpp_aliquota,
                    "valor": self.retencao_cpp_valor,
                }
            },
            "tributavel": self.tributavel,
            "ibpt": {
                "simplificado": {
                    "aliquota": self.ibpt_simplificado_aliquota,
                },
                "detalhado": {
                    "aliquota": {
                        "municipal": self.ibpt_detalhado_aliquota_municipal,
                        "estadual": self.ibpt_detalhado_aliquota_estadual,
                        "federal": self.ibpt_detalhado_aliquota_federal,
                    }
                }
            },
            "responsavelRetencao": self.responsavel_retencao,
            "tributosFederaisRetidos": self.tributos_federais_retidos,
        }

        return servico_dict

def mongo_to_dict(mongo_obj):
    servico_dict = {
        "codigo": mongo_obj['codigo'],
        "id_integracao": mongo_obj['idIntegracao'],
        "discriminacao": mongo_obj['discriminacao'],
        "codigo_tributacao": mongo_obj['codigoTributacao'],
        "cnae": mongo_obj['cnae'],
        "codigo_cidade_incidencia": mongo_obj['codigoCidadeIncidencia'],
        "descricao_cidade_incidencia": mongo_obj['descricaoCidadeIncidencia'],
        "unidade": mongo_obj['unidade'],
        "quantidade": mongo_obj['quantidade'],
        "iss_tipo_tributacao": mongo_obj['iss']['tipoTributacao'],
        "iss_exigibilidade": mongo_obj['iss']['exigibilidade'],
        "iss_retido": mongo_obj['iss']['retido'],
        "iss_aliquota": mongo_obj['iss']['aliquota'],
        "iss_valor": mongo_obj['iss']['valor'],
        "iss_valor_retido": mongo_obj['iss']['valorRetido'],
        "iss_processo_suspensao": mongo_obj['iss']['processoSuspensao'],
        "obra_art": mongo_obj['obra']['art'],
        "obra_codigo": mongo_obj['obra']['codigo'],
        "obra_cei": mongo_obj['obra']['cei'],
        "valor_servico": mongo_obj['valor']['servico'],
        "valor_base_calculo": mongo_obj['valor']['baseCalculo'],
        "valor_deducoes": mongo_obj['valor']['deducoes'],
        "valor_desconto_condicionado": mongo_obj['valor']['descontoCondicionado'],
        "valor_desconto_incondicionado": mongo_obj['valor']['descontoIncondicionado'],
        "valor_liquido": mongo_obj['valor']['liquido'],
        "valor_unitario": mongo_obj['valor']['unitario'],
        "valor_aproximado_tributos": mongo_obj['valor']['valorAproximadoTributos'],
        "deducao_tipo": mongo_obj['deducao']['tipo'],
        "deducao_descricao": mongo_obj['deducao']['descricao'],
        "retencao_pis_base_calculo": mongo_obj['retencao']['pis']['baseCalculo'],
        "retencao_pis_aliquota": mongo_obj['retencao']['pis']['aliquota'],
        "retencao_pis_valor": mongo_obj['retencao']['pis']['valor'],
        "retencao_pis_cst": mongo_obj['retencao']['pis']['cst'],
        "retencao_cofins_base_calculo": mongo_obj['retencao']['cofins']['baseCalculo'],
        "retencao_cofins_aliquota": mongo_obj['retencao']['cofins']['aliquota'],
        "retencao_cofins_valor": mongo_obj['retencao']['cofins']['valor'],
        "retencao_cofins_cst": mongo_obj['retencao']['cofins']['cst'],
        "retencao_csll_aliquota": mongo_obj['retencao']['csll']['aliquota'],
        "retencao_csll_valor": mongo_obj['retencao']['csll']['valor'],
        "retencao_inss_aliquota": mongo_obj['retencao']['inss']['aliquota'],
        "retencao_inss_valor": mongo_obj['retencao']['inss']['valor'],
        "retencao_irrf_aliquota": mongo_obj['retencao']['irrf']['aliquota'],
        "retencao_irrf_valor": mongo_obj['retencao']['irrf']['valor'],
        "retencao_cpp_aliquota": mongo_obj['retencao']['cpp']['aliquota'],
        "retencao_cpp_valor": mongo_obj['retencao']['cpp']['valor'],
        "outrasRetencoes": mongo_obj['retencao']['outrasRetencoes'],
        "tributavel": mongo_obj['tributavel'],
        "ibpt_simplificado_aliquota": mongo_obj['ibpt']['simplificado']['aliquota'],
        "ibpt_detalhado_aliquota_municipal": mongo_obj['ibpt']['detalhado']['aliquota']['municipal'],
        "ibpt_detalhado_aliquota_estadual": mongo_obj['ibpt']['detalhado']['aliquota']['estadual'],
        "ibpt_detalhado_aliquota_federal": mongo_obj['ibpt']['detalhado']['aliquota']['federal'],
        "responsavel_retencao": mongo_obj['responsavelRetencao'],
        "tributos_federais_retidos": mongo_obj['tributosFederaisRetidos'],
    }

    return servico_dict