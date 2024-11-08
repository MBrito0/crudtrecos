# Funções de uso geral no aplicativo

from datetime import date, datetime


def remove_prefixo(d):
    """
    Remove o prefixo das chaves de um dicionário.
    :param d: dicionário original com prefixo nas chaves
    :return: novo dicionário com as chaves sem o prefixo
    """
    # Obtém o prefixo a partir da primeira chave do dicionário
    first_key = next(iter(d))
    prefix = first_key.split('_')[0] + '_'

    # Cria um novo dicionário com as chaves sem o prefixo
    new_dict = {key[len(prefix):]: value for key, value in d.items()}
    return new_dict


def datetime_para_string(data):
    """
    Converte todos os objetos datetime em texto no dicionário fornecido.
    """
    for key, value in data.items():
        if isinstance(value, datetime):
            # Converte datetime para string ISO 8601
            data[key] = value.isoformat()
        elif isinstance(value, date):
            data[key] = value.isoformat()  # Converte date para string ISO 8601
    return data
