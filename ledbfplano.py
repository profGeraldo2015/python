from dbfread import DBF
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="scnovo2021"
)

mycursor = conn.cursor()
# Especifique o caminho do arquivo DBF
#caminho_arquivo = './ARQPLANC.DBF'
caminho_arquivo = 'F:\\GERALDO2023\\VM\\ARQPLANC.DBF'

registros_lidos = 0
registros_erroslidos = 0
#tabela sc-php planos, tabela api-maransato/menudash plano
tabela = 'planos'
sql = "TRUNCATE TABLE "+tabela
print(sql)

if tabela == 'plano':
    campos = 'numero,descricao,saldo_inic,dt_saldo,saldo_iniv,dt_saus,c_saieus,c_saivus'
else:
    campos = 'NUMERO,DESCRICAO,SALDO_INIC,DT_SALDO,SALDO_INIV,DT_SAUS,C_SAIEUS,C_SAIVUS'

sqlInsert = "INSERT INTO "+tabela+" ("+campos+") VALUES (%s, %s, %s,%s, %s, %s, %s, %s)"
print(sqlInsert)
mycursor.execute(sql)
# Abre o arquivo DBF
with DBF(caminho_arquivo, encoding='latin1') as dbf:
    # Itera sobre os registros do arquivo DBF
    nomes_campos = dbf.field_names
    print(nomes_campos)
    try:
       for record in dbf:
        # Insere o registro na tabela MySQL
        mycursor.execute(sqlInsert,(record['NUMERO'], record['DESCRICAO'], record['SALDO_INIC'],record['DT_SALDO'] ,record['SALDO_INIV'],record['DT_SAUS'], record['C_SAIEUS'], record['C_SAIVUS']))
        
#        for campo in nomes_campos:
                #print(f" {campo}: {record[campo]}")
                #print()
        registros_lidos += 1
    except Exception as e:
        print("Erro na linha:", e, record)    
        registros_erroslidos += 1
                
print(f"Total de registros lidos: {registros_lidos}")
print(f"Total de registros com erro: {registros_erroslidos}")
       
# Confirma as alterações
conn.commit()
