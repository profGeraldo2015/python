import mysql.connector
import locale
#le arquivo balance.txt e atualiza o saldo inicial na tabela planos
# Configurar o locale para o formato brasileiro
locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')

def converter_numero(valor):
    try:
        valor_limpo = valor.replace('.', '').replace(',', '.')
        return float(valor_limpo)
    except ValueError:
        print(f"Erro ao converter o valor: {valor}")
        return 0.0

def ler_balance():
    # Definir as posições dos campos
    POSICAO_CONTA = (0, 8)    # Primeiros 8 caracteres
    POSICAO_VALOR = (48, 65)  # Posição 48 até 65

    try:
        with open('balance.txt', 'r') as arquivo:
            for linha in arquivo:
                # Extrai a conta (primeiros 8 caracteres)
                conta = linha[POSICAO_CONTA[0]:POSICAO_CONTA[1]].strip()
                
                # Extrai o valor (posição 48 até 65)
                valor = linha[POSICAO_VALOR[0]:POSICAO_VALOR[1]].strip()
                
                # Imprime os campos
                print(f"Conta: {conta} | Valor: {valor}")
                
    except FileNotFoundError:
        print("Arquivo balance.txt não encontrado!")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")

def atualizar_saldo():
    try:
        # Conectar ao banco de dados MySQL
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="scnovo2021"
        )
        
        cursor = conexao.cursor()

        # Definir as posições dos campos
        POSICAO_CONTA = (0, 8)    # Primeiros 8 caracteres
        POSICAO_VALOR = (48, 65)  # Posição 48 até 65

        with open('balance.txt', 'r') as arquivo:
            for linha in arquivo:
                # Extrai a conta e valor
                conta = linha[POSICAO_CONTA[0]:POSICAO_CONTA[1]].strip()
                valor = linha[POSICAO_VALOR[0]:POSICAO_VALOR[1]].strip()
                valor_convertido = converter_numero(valor)

                # Query SQL para atualizar o SALDO_INIV
                sql = """
                UPDATE planos 
                SET SALDO_INIV = %s 
                WHERE NUMERO = %s
                """
                
                dados = (valor_convertido, conta)
                cursor.execute(sql, dados)
                print(f"Conta {conta} atualizada com valor {valor_convertido}")

        # Commit e fechamento da conexão
        conexao.commit()
        print("Atualização concluída com sucesso!")

    except FileNotFoundError:
        print("Arquivo balance.txt não encontrado!")
    except mysql.connector.Error as err:
        print(f"Erro no banco de dados: {err}")
    except Exception as e:
        print(f"Erro: {str(e)}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão com o banco encerrada")

if __name__ == "__main__":
    ler_balance()
    atualizar_saldo()