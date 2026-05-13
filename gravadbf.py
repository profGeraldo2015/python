from dbfread import DBF
from dbf import Table

# Caminho para o arquivo DBF
dbf_file = 'exemplo.dbf'

# Dados a serem gravados no arquivo DBF
dados = [
    {'ID': 1, 'Nome': 'João', 'Idade': 30},
    {'ID': 2, 'Nome': 'Maria', 'Idade': 25},
    {'ID': 3, 'Nome': 'José', 'Idade': 35}
]

# Cria uma nova tabela DBF
tabela = Table(dbf_file, 'w')

# Adiciona os campos à tabela
tabela.add_fields('ID C(10); Nome C(50); Idade N(3,0)')

# Insere os dados na tabela
for dado in dados:
    tabela.append(dado)

# Fecha a tabela
tabela.close()

print("Dados gravados com sucesso no arquivo DBF.")
