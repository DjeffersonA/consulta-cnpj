# Sistema de Consulta Massiva de CNPJs

Sistema feito para realizar consultas massivas de CNPJs, utilizando a API MinhaReceita, e guardar as informações em um arquivo CSV.

## Modo de Uso: 

1. Inserir os CNPJs no arquivo "data.csv" (um CNPJ por coluna) e salvar.
2. Executar o arquivo "cnpj.py"

### OBS.: Não deixar o arquivo "cnpj.csv" aberto durante a execução do cnpj.py.

## Informações obtidas:

1. CNPJ, Razão Social, Nome fantasia
2. Data de abertura, Porte, Natureza jurídica, Tipo, CNAE
3. Endereço, Número, Complemento, Bairro, CEP, Município, UF
4. Telefone 1, Telefone 2

Programa utilizado primariamente com auxílio da base de dados públicos de CNPJ disponibilizados pela Receita Federal.
