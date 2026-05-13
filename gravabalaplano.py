import mysql.connector
import locale

# Configurar o locale para o formato brasileiro
locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')
# Função para converter o número do formato brasileiro para o formato MySQL
def converter_numero(valor):
    try:
        # Remove o ponto de milhar e substitui a vírgula por ponto
        valor_limpo = valor.replace('.', '').replace(',', '.')
        # Converte para float
        return float(valor_limpo)
    except ValueError:
        print(f"Erro ao converter o valor: {valor}")
        return 0.0  # ou outro valor padrão


# Conectar ao banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="scnovo2021"
)

cursor = conexao.cursor()

# cursor.execute('TRUNCATE TABLE PLANOS2')

# Definir as posições dos campos (início, fim)
campos = [
    (0, 8),   # Campo 1: caracteres 0-9
    (48, 65)   # Campo 2: caracteres 20-29
]

data_atual = '2024-12-31'

# Ler o arquivo TXT
with open('balance.txt', 'r') as arquivo:
    for linha in arquivo:
        # Extrair dados usando as posições definidas
        dados = [linha[inicio:fim].strip() for inicio, fim in campos]
        
        dados[1]=converter_numero(dados[1])
        
        # inseriu dt_saldo fixo
        dados.append(data_atual)
        # inseriu saldo_iniv
        dados.append(dados[1])
        # INSERIU DT_SAUS E C_SAIEUS E C_SAIVUS FIXOS
        dados.append(data_atual)
        dados.append(dados[1])
        dados.append(dados[1])
        #dados.append(dados[0])
        
        
        # Criar a query SQL
        #sql = "INSERT INTO PLANOS2 (NUMERO, DESCRICAO, SALDO_INIC,DT_SALDO,SALDO_INIV,DT_SAUS,C_SAIEUS,C_SAIVUS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        sql = """
        UPDATE planos
        SET SALDO_INIC = %s, DT_SALDO = %s, SALDO_INIV = %s,DT_SAUS=%s,C_SAIEUS=%s,C_SAIVUS=%s
        WHERE NUMERO = %s
        """
        print(sql)
        print(dados)
        dados_update = (dados[1],dados[2],dados[3],dados[4],dados[5],dados[6],dados[0])
        print(dados_update)
        
        # Executar a query, linha tirada em 09022026 por achar que não está alterando no db
        #cursor.execute(sql, dados_update)

# Commit das mudanças e fechar a conexão
conexao.commit()
conexao.close()

print("Dados saldo inicial atualizados com sucesso!")
