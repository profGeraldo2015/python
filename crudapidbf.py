from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
import dbf

app = FastAPI()

ARQUIVO_DBF = 'AMOVCONT.DBF'
tabela = dbf.Table(ARQUIVO_DBF, codepage='cp1252')
tabela.open(mode=dbf.READ_WRITE)


# Altere os campos abaixo de acordo com sua estrutura real
#table_fields = [field.name for field in tabela.field_names]

# Exemplo genérico: substitua por sua estrutura real
class Registro(BaseModel):
    DT_EMISSAO: date
    DT_VENCTO: date
    CT_DEBITO: str
    CT_CREDITO: str
    VALOR10: float
    VALORUS: float
    HIST: str  # Suponha que 'CODIGO' seja um campo de identificação ÚNI
    OBS: str
    FONTE: str
    STATUS: str

@app.get("/registros")
def listar_registros():
    registros = []
    for r in tabela:
        if not dbf.is_deleted(r):
            registro = {}
            for field in tabela.field_names:
                try:
                    valor = getattr(r, field)
                except UnicodeDecodeError:
                    valor = "<erro de codificação>"
                registro[field] = valor
            registros.append(registro)
    return registros

@app.post("/registros")
def inserir_registro(registro: Registro):
    tabela.append(registro.dict())
    return {"mensagem": "Registro inserido com sucesso."}

@app.put("/registros/{codigo}")
def atualizar_registro(codigo: str, dados: Registro):
    for r in tabela:
        if not r.deleted and r.CODIGO == codigo:
            with dbf.at(record=r):
                for campo, valor in dados.dict().items():
                    setattr(r, campo, valor)
            return {"mensagem": "Registro atualizado com sucesso."}
    raise HTTPException(status_code=404, detail="Registro não encontrado")

@app.delete("/registros/{codigo}")
def deletar_registro(codigo: str):
    for r in tabela:
        if not r.deleted and r.CODIGO == codigo:
            r.delete()
            return {"mensagem": "Registro deletado com sucesso."}
    raise HTTPException(status_code=404, detail="Registro não encontrado")
