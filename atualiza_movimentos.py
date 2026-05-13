from dbfread import DBF
from datetime import datetime
import mysql.connector

def conectar_banco():
    """Conecta ao banco de dados MySQL"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="scnovo2021"
    )

def verificar_registro_existe(cursor, dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor):
    """Verifica se um registro já existe na tabela movimentos"""
    sql_verificar = """
    SELECT COUNT(*) FROM movimentos 
    WHERE DT_EMISSAO = %s 
    AND CT_DEBITO = %s 
    AND CT_CREDITO = %s 
    AND HIST = %s 
    AND OBS = %s 
    AND DT_VENCTO = %s 
    AND VALOR10 = %s
    """
    cursor.execute(sql_verificar, (dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor))
    return cursor.fetchone()[0] > 0

def atualizar_movimentos(caminho_arquivo_dbf):
    """Atualiza a tabela movimentos com registros que não existem"""
    
    # Conecta ao banco
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # Configurações
    tabela = 'movimentos'
    campos = 'DT_EMISSAO,CT_DEBITO,CT_CREDITO,HIST,OBS,DT_VENCTO,VALOR10'
    sql_insert = f"INSERT INTO {tabela} ({campos}) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    # Contadores
    registros_lidos = 0
    registros_gravados = 0
    registros_existentes = 0
    registros_erros = 0
    
    print(f"Iniciando atualização da tabela {tabela}")
    print(f"Arquivo DBF: {caminho_arquivo_dbf}")
    print(f"SQL Insert: {sql_insert}")
    print("-" * 50)
    
    try:
        # Abre o arquivo DBF
        with DBF(caminho_arquivo_dbf, encoding='latin1') as dbf:
            nomes_campos = dbf.field_names
            print(f"Campos encontrados no DBF: {nomes_campos}")
            print("-" * 50)
            
            for record in dbf:
                try:
                    registros_lidos += 1
                    
                    # Extrai os valores do registro
                    dt_emissao = record['DT_EMISSAO']
                    ct_debito = record['CT_DEBITO']
                    ct_credito = record['CT_CREDITO']
                    hist = record['HIST']
                    obs = record['OBS']
                    dt_vencto = record['DT_VENCTO']
                    valor = record['VALORUS']  # Assumindo que é VALORUS baseado no código original
                    
                    # Verifica se o registro já existe
                    if verificar_registro_existe(cursor, dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor):
                        registros_existentes += 1
                        if registros_existentes % 100 == 0:
                            print(f"Registros existentes encontrados: {registros_existentes}")
                    else:
                        # Insere o novo registro
                        if dt_vencto.year == 2025:
                            cursor.execute(sql_insert, (dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor))
                            registros_gravados += 1
                        
                        if registros_gravados % 100 == 0:
                            print(f"Registros gravados: {registros_gravados}")
                    
                    # Mostra progresso a cada 1000 registros
                    if registros_lidos % 1000 == 0:
                        print(f"Progresso: {registros_lidos} registros processados")
                        
                except Exception as e:
                    registros_erros += 1
                    print(f"Erro ao processar registro {registros_lidos}: {e}")
                    print(f"Registro: {record}")
                    continue
    
    except Exception as e:
        print(f"Erro ao abrir arquivo DBF: {e}")
        return
    
    finally:
        # Confirma as alterações
        conn.commit()
        cursor.close()
        conn.close()
    
    # Relatório final
    print("-" * 50)
    print("RELATÓRIO FINAL")
    print("-" * 50)
    print(f"Total de registros lidos do DBF: {registros_lidos}")
    print(f"Total de registros já existentes: {registros_existentes}")
    print(f"Total de novos registros gravados: {registros_gravados}")
    print(f"Total de registros com erro: {registros_erros}")
    print(f"Taxa de sucesso: {((registros_gravados + registros_existentes) / registros_lidos * 100):.2f}%")

if __name__ == "__main__":
    # Especifique o caminho do arquivo DBF
    caminho_arquivo = 'F:\\GERALDO2023\\VM\\AMOVCONT.DBF'
    
    # Executa a atualização
    atualizar_movimentos(caminho_arquivo) 