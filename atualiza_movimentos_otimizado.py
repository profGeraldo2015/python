from dbfread import DBF
from datetime import datetime
import mysql.connector
import hashlib

def conectar_banco():
    """Conecta ao banco de dados MySQL"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="scnovo2021"
    )

def criar_hash_registro(dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor):
    """Cria um hash único para identificar o registro"""
    registro_str = f"{dt_emissao}{ct_debito}{ct_credito}{hist}{obs}{dt_vencto}{valor}"
    return hashlib.md5(registro_str.encode('utf-8')).hexdigest()

def carregar_registros_existentes(cursor):
    """Carrega todos os registros existentes da tabela movimentos em um set para busca rápida"""
    print("Carregando registros existentes da tabela movimentos...")
    
    sql_select = """
    SELECT DT_EMISSAO, CT_DEBITO, CT_CREDITO, HIST, OBS, DT_VENCTO, VALOR10 
    FROM movimentos
    """
    
    cursor.execute(sql_select)
    registros_existentes = set()
    
    for row in cursor.fetchall():
        dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor = row
        hash_registro = criar_hash_registro(dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor)
        registros_existentes.add(hash_registro)
    
    print(f"Carregados {len(registros_existentes)} registros existentes")
    return registros_existentes

def atualizar_movimentos_otimizado(caminho_arquivo_dbf):
    """Atualiza a tabela movimentos com registros que não existem (versão otimizada)"""
    
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
    
    print(f"Iniciando atualização otimizada da tabela {tabela}")
    print(f"Arquivo DBF: {caminho_arquivo_dbf}")
    print("-" * 50)
    
    try:
        # Carrega registros existentes em memória
        registros_existentes_set = carregar_registros_existentes(cursor)
        
        # Abre o arquivo DBF
        with DBF(caminho_arquivo_dbf, encoding='latin1') as dbf:
            nomes_campos = dbf.field_names
            print(f"Campos encontrados no DBF: {nomes_campos}")
            print("-" * 50)
            
            # Lista para armazenar novos registros para inserção em lote
            novos_registros = []
            
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
                    
                    # Cria hash do registro atual
                    hash_registro = criar_hash_registro(dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor)
                    
                    # Verifica se o registro já existe
                    if hash_registro in registros_existentes_set:
                        registros_existentes += 1
                        if registros_existentes % 1000 == 0:
                            print(f"Registros existentes encontrados: {registros_existentes}")
                    else:
                        # Adiciona à lista de novos registros
                        novos_registros.append((dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor))
                        
                        # Insere em lote a cada 1000 registros para melhor performance
                        if len(novos_registros) >= 1000:
                            cursor.executemany(sql_insert, novos_registros)
                            registros_gravados += len(novos_registros)
                            print(f"Lote inserido: {len(novos_registros)} registros (Total: {registros_gravados})")
                            novos_registros = []
                    
                    # Mostra progresso a cada 5000 registros
                    if registros_lidos % 5000 == 0:
                        print(f"Progresso: {registros_lidos} registros processados")
                        
                except Exception as e:
                    registros_erros += 1
                    print(f"Erro ao processar registro {registros_lidos}: {e}")
                    print(f"Registro: {record}")
                    continue
            
            # Insere registros restantes
            if novos_registros:
                cursor.executemany(sql_insert, novos_registros)
                registros_gravados += len(novos_registros)
                print(f"Lote final inserido: {len(novos_registros)} registros")
    
    except Exception as e:
        print(f"Erro ao processar arquivo DBF: {e}")
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
    if registros_lidos > 0:
        print(f"Taxa de sucesso: {((registros_gravados + registros_existentes) / registros_lidos * 100):.2f}%")
        print(f"Taxa de novos registros: {(registros_gravados / registros_lidos * 100):.2f}%")

def atualizar_movimentos_com_filtro(caminho_arquivo_dbf, ano_filtro=None):
    """Atualiza a tabela movimentos com filtro opcional por ano"""
    
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
    registros_filtrados = 0
    
    print(f"Iniciando atualização da tabela {tabela}")
    if ano_filtro:
        print(f"Filtro aplicado: apenas registros do ano {ano_filtro}")
    print(f"Arquivo DBF: {caminho_arquivo_dbf}")
    print("-" * 50)
    
    try:
        # Carrega registros existentes em memória
        registros_existentes_set = carregar_registros_existentes(cursor)
        
        # Abre o arquivo DBF
        with DBF(caminho_arquivo_dbf, encoding='latin1') as dbf:
            nomes_campos = dbf.field_names
            print(f"Campos encontrados no DBF: {nomes_campos}")
            print("-" * 50)
            
            # Lista para armazenar novos registros para inserção em lote
            novos_registros = []
            
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
                    valor = record['VALORUS']
                    
                    # Aplica filtro por ano se especificado
                    if ano_filtro and dt_vencto.year != ano_filtro:
                        registros_filtrados += 1
                        continue
                    
                    # Cria hash do registro atual
                    hash_registro = criar_hash_registro(dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor)
                    
                    # Verifica se o registro já existe
                    if hash_registro in registros_existentes_set:
                        registros_existentes += 1
                        if registros_existentes % 1000 == 0:
                            print(f"Registros existentes encontrados: {registros_existentes}")
                    else:
                        # Adiciona à lista de novos registros
                        novos_registros.append((dt_emissao, ct_debito, ct_credito, hist, obs, dt_vencto, valor))
                        
                        # Insere em lote a cada 1000 registros
                        if len(novos_registros) >= 1000:
                            cursor.executemany(sql_insert, novos_registros)
                            registros_gravados += len(novos_registros)
                            print(f"Lote inserido: {len(novos_registros)} registros (Total: {registros_gravados})")
                            novos_registros = []
                    
                    # Mostra progresso a cada 5000 registros
                    if registros_lidos % 5000 == 0:
                        print(f"Progresso: {registros_lidos} registros processados")
                        
                except Exception as e:
                    registros_erros += 1
                    print(f"Erro ao processar registro {registros_lidos}: {e}")
                    continue
            
            # Insere registros restantes
            if novos_registros:
                cursor.executemany(sql_insert, novos_registros)
                registros_gravados += len(novos_registros)
                print(f"Lote final inserido: {len(novos_registros)} registros")
    
    except Exception as e:
        print(f"Erro ao processar arquivo DBF: {e}")
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
    if ano_filtro:
        print(f"Registros filtrados (não {ano_filtro}): {registros_filtrados}")
    print(f"Total de registros já existentes: {registros_existentes}")
    print(f"Total de novos registros gravados: {registros_gravados}")
    print(f"Total de registros com erro: {registros_erros}")
    if registros_lidos > 0:
        registros_processados = registros_lidos - registros_filtrados
        print(f"Taxa de sucesso: {((registros_gravados + registros_existentes) / registros_processados * 100):.2f}%")
        print(f"Taxa de novos registros: {(registros_gravados / registros_processados * 100):.2f}%")

if __name__ == "__main__":
    # Especifique o caminho do arquivo DBF
    caminho_arquivo = 'F:\\GERALDO2023\\VM\\AMOVCONT.DBF'
    
    # Executa a atualização (escolha uma das opções abaixo)
    
    # Opção 1: Atualização completa
    print("=== ATUALIZAÇÃO COMPLETA ===")
    atualizar_movimentos_otimizado(caminho_arquivo)
    
    # Opção 2: Atualização com filtro por ano (descomente se quiser usar)
    # print("\n=== ATUALIZAÇÃO COM FILTRO ANO 2025 ===")
    # atualizar_movimentos_com_filtro(caminho_arquivo, ano_filtro=2025) 