import os

def buscar_arquivos_por_nome(diretorio_base, palavra_chave=None):
    resultados = []
    for root, dirs, files in os.walk(diretorio_base):
        for file in files:
            if palavra_chave is None or palavra_chave.lower() in file.lower():
                caminho_completo = os.path.join(root, file)
                tamanho = os.path.getsize(caminho_completo)
                resultados.append((caminho_completo, tamanho))
    return resultados

# Definições
DIRETORIO_BASE = "Z:\\GERALDO"  # Altere para o caminho desejado
ARQUIVO_SAIDA = "resultadoconfia.txt"
PALAVRA_CHAVE = "confia"  # Altere para a palavra desejada

if __name__ == "__main__":
    resultados = buscar_arquivos_por_nome(DIRETORIO_BASE, PALAVRA_CHAVE)
    with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
        for caminho, tamanho in resultados:
            f.write(f"{caminho}: {tamanho} bytes\n")
    print(f"Busca concluída! Resultados salvos em '{ARQUIVO_SAIDA}'.")