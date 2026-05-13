import dbf

# Abrindo o arquivo
tabela = dbf.Table('F:/GERALDO2023/VM/AMOVCONT.DBF')
                   
tabela.open(mode=dbf.READ_ONLY)

# Mostrar estrutura
print("Estrutura da tabela:")
print(tabela.structure())

# Listar os primeiros registros (para referência)
print("\nAlguns registros:")
for i, registro in enumerate(tabela):
    if i >= 5:
        break
    print(registro)

tabela.close()
