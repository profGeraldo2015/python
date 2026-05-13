import mysql.connector
import locale

# Configurar o locale para o formato brasileiro
locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')

# Função para converter o número do formato brasileiro para o formato MySQL
def converter_numero(valor):
    try:
        valor_limpo = valor.replace('.', '').replace(',', '.')
        return float(valor_limpo)
    except ValueError:
        print(f"Erro ao converter o valor: {valor}")
        return 0.0

# Conectar ao banco de dados MySQL
conexao = mysql.connector.connect(
    host="seu_host",
    user="seu_usuario",
    password="sua_senha",
    database="seu_banco_de_dados"
)

cursor = conexao.cursor()

# Definir as posições dos campos (início, fim)
campos = [
    (0, 10),   # Campo 1: caracteres 0-9 (chave única)
    (10, 20),  # Campo 2: caracteres 10-19 (campo numérico)
    (20, 30)   # Campo 3: caracteres 20-29
]

# Data específica a ser atualizada
data_especifica = '2020-12-31'

# Ler o arquivo TXT
with open('seu_arquivo.txt', 'r') as arquivo:
    for linha in arquivo:
        # Extrair dados usando as posições definidas
        dados = [linha[inicio:fim].strip() for inicio, fim in campos]
        
        # Converter o campo numérico (assumindo que é o segundo campo)
        dados[1] = converter_numero(dados[1])
        
        # Criar a query SQL para UPDATE
        sql = """
        UPDATE sua_tabela 
        SET coluna2 = %s, coluna3 = %s, data = %s
        WHERE coluna1 = %s
        """
        
        # Preparar os dados para a query (na ordem: coluna2, coluna3, data, coluna1)
        dados_update = (dados[1], dados[2], data_especifica, dados[0])
        
        # Executar a query
        cursor.execute(sql, dados_update)

# Commit das mudanças e fechar a conexão
conexao.commit()
conexao.close()

print("Dados atualizados com sucesso!")