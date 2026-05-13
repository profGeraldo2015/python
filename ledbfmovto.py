from dbfread import DBF
from datetime import datetime
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="scnovo2021"
)

mycursor = conn.cursor()
# Especifique o caminho do arquivo DBF
caminho_arquivo = 'F:\\GERALDO2023\\VM\\AMOVCONT.DBF'

registros_lidos = 0
registros_gravados = 0
registros_erroslidos = 0
#TABELA movimentos PARA SC-PHP, movimento para api maransato(node)/menudash(next)
tabela = 'movimentos'
#para tabela movimento colocar 1990 para gravar todos os registros
ano = 2025

sql = "TRUNCATE TABLE "+tabela

print(sql)

mycursor.execute(sql)

if tabela == 'movimento':
    campos = 'dt_emissao,debito,credito,hist, obs,dt_vencto, valor'
    ano = 1990 
else:
    campos = 'DT_EMISSAO,CT_DEBITO,CT_CREDITO,HIST,OBS,DT_VENCTO, VALOR10'
    ano = 2025
sqlInsert = "INSERT INTO "+tabela+" ("+campos+") VALUES (%s, %s, %s, %s, %s, %s, %s) "

print(sqlInsert)

# Abre o arquivo DBF
with DBF(caminho_arquivo, encoding='latin1') as dbf:
    # Itera sobre os registros do arquivo DBF
    nomes_campos = dbf.field_names
    print(nomes_campos)
    try:
       for record in dbf:
        # Insere o registro na tabela MySQL
#        mycursor.execute("INSERT INTO movimento (dt_emissao,debito,credito,hist, obs,dt_vencto, valor) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
        
        #print(f"Registro inserido: - {record['DT_VENCTO']} - {record['VALORUS']}")
        
        data_vencto = record['DT_VENCTO']
        
        if data_vencto.year >= ano:
            #print(f"Data de vencimento convertida: {data_vencto.year}")
            
            mycursor.execute(sqlInsert,(record['DT_EMISSAO'], record['CT_DEBITO'], record['CT_CREDITO'], record['HIST'], record['OBS'], record['DT_VENCTO'], record['VALORUS']))
            
            registros_gravados += 1
        #else:
            
            #print(f"Data de vencimento: {data_vencto.year}")
            
        
        #mycursor.execute("INSERT INTO movimentos (DT_EMISSAO,CT_DEBITO,CT_CREDITO,HIST,OBS,DT_VENCTO, VALOR10) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
        
#        for campo in nomes_campos:
                #print(f" {campo}: {record[campo]}")
                #print()
        registros_lidos += 1
    except Exception as e:
        print("Erro na linha:", e, record)    
        registros_erroslidos += 1
                
print(f"Total de registros lidos: {registros_lidos}")
print(f"Total de registros gravados: {registros_gravados}")

print(f"Total de registros com erro: {registros_erroslidos}")


        
# Confirma as alterações
conn.commit()
