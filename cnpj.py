import json
import sys
import urllib.request
import csv
import pandas as pd
import os
from tqdm import tqdm 

def valida_cnpj(cnpj):
    cnpj = parse_input(cnpj)
    if len(cnpj) != 14 or not cnpj.isnumeric():
        return False

    verificadores = cnpj[-2:]
    lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    soma = 0
    for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-2]))):
        soma += int(numero) * int(lista_validacao_um[ind])
    soma = soma % 11
    digito_um = 0 if soma < 2 else 11 - soma

    soma = 0
    for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-1]))):
        soma += int(numero) * int(lista_validacao_dois[ind])
    soma = soma % 11
    digito_dois = 0 if soma < 2 else 11 - soma

    return verificadores == str(digito_um) + str(digito_dois)

def parse_input(i):
    i = str(i)
    i = i.replace('.', '')
    i = i.replace(',', '')
    i = i.replace('/', '')
    i = i.replace('-', '')
    i = i.replace("'", '')
    i = i.replace('[', '')
    i = i.replace(']', '')
    i = i.replace('\\', '')
    return i

def busca_cnpj(cnpj):
    url = 'https://minhareceita.org/{0}'.format(cnpj)
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent',
         " Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0")]

    with opener.open(url) as fd:
        content = fd.read().decode()

    dic = json.loads(content)

    if dic['cnpj'] == 0:
        print('CNPJ {0} rejeitado pela Receita Federal\n'.format(cnpj))
    else:
        try:
            with open('cnpj.csv', 'a', newline='') as file:
                fieldnames = fieldnames = ['CNPJ', 'Nome', 'Nome fantasia', 'Data de abertura', 'Porte', 'Natureza jurídica', 'Tipo', 'CNAE', 'Endereço', 'Número', 'Complemento', 'Bairro', 'CEP', 'Município', 'UF', 'Telefone 1', 'Telefone 2']
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
                if format(dic['identificador_matriz_filial']) == '1':
                    identi = 'MATRIZ'
                else:
                    identi = 'FILIAL'
                writer.writerow({'CNPJ': format(dic['cnpj']), 'Nome': format(dic['razao_social']), 'Nome fantasia': format(dic['nome_fantasia']), 'Data de abertura': format(dic['data_inicio_atividade']), 'Porte': format(dic['porte']), 'Natureza jurídica': format(dic['natureza_juridica']), 'Tipo': format(identi), 'CNAE': format(dic['cnae_fiscal'])+' - '+format(dic['cnae_fiscal_descricao']), 'Endereço': format(dic['descricao_tipo_de_logradouro'])+' '+format(dic['logradouro']), 'Número': format(dic['numero']), 'Complemento': format(dic['complemento']), 'Bairro': format(dic['bairro']), 'CEP': format(dic['cep']), 'Município': format(dic['municipio']), 'UF': format(dic['uf']), 'Telefone 1': format(dic['ddd_telefone_1']), 'Telefone 2': format(dic['ddd_telefone_2'])})
        except KeyError:
            pass

def row_count(input):
    with open(input, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i

if __name__ == '__main__':
    os.system('cls')
    count = 0
    print('\n   RECEITA FEDERAL                                      | CONSULTA CNPJ\n')

    with open('data.csv', 'r') as csv_file:
        lines = len(csv_file.readlines())

    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in tqdm(reader, total=lines, bar_format=' {l_bar}{bar:50}| {n_fmt}/{total_fmt} [ Tempo restante estimado: {remaining} ]'):
            if valida_cnpj(row):
                busca_cnpj(parse_input(row))
                count = count+1
        print('\nTotal de '+str(count)+' CNPJs consultados.\n')
    input('Pressione Enter para finalizar o programa...')
