import os

def calcular_tamanho_pasta_por_nome(diretorio, palavra_chave=None):
    total_tamanho = 0
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            if palavra_chave is None or palavra_chave.lower() in file.lower():
                caminho_completo = os.path.join(root, file)
                total_tamanho += os.path.getsize(caminho_completo)
    return total_tamanho

def buscar_pastas_com_tamanho_por_nome(diretorio_base, palavra_chave=None):
    resultados = []
    for root, dirs, files in os.walk(diretorio_base):
        tamanho_pasta = 0
        for file in files:
            if palavra_chave is None or palavra_chave.lower() in file.lower():
                caminho_completo = os.path.join(root, file)
                tamanho_pasta += os.path.getsize(caminho_completo)
        if tamanho_pasta > 0:
            resultados.append((root, tamanho_pasta))
    return resultados

# Definições
DIRETORIO_BASE = "F:\\Geraldo\\desenv"  # Altere para o caminho desejado
ARQUIVO_SAIDA = "resultados.txt"
PALAVRA_CHAVE = "verdadeira"  # Altere para a palavra desejada

if __name__ == "__main__":
    resultados = buscar_pastas_com_tamanho_por_nome(DIRETORIO_BASE, PALAVRA_CHAVE)
    with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
        for caminho, tamanho in resultados:
            f.write(f"{caminho}: {tamanho} bytes\n")
    print(f"Busca concluída! Resultados salvos em '{ARQUIVO_SAIDA}'.")