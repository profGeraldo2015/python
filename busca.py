import os

def buscar_arquivos(diretorio_base, extensoes, arquivo_saida):
    """
    Busca arquivos com as extensões especificadas em um diretório e grava o resultado em um arquivo texto.

    :param diretorio_base: Caminho do diretório base para a busca.
    :param extensoes: Lista de extensões de arquivos a serem procuradas (ex: ['.txt', '.py']).
    :param arquivo_saida: Nome do arquivo onde serão gravados os resultados.
    """
    resultados = []

    # Percorre o diretório e subdiretórios
    for root, dirs, files in os.walk(diretorio_base):
        for file in files:
            if any(file.endswith(ext) for ext in extensoes):
                caminho_completo = os.path.join(root, file)
                resultados.append(caminho_completo)

    # Grava os resultados no arquivo de saída
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for caminho in resultados:
            f.write(caminho + '\n')

    print(f"Busca concluída! Resultados salvos em '{arquivo_saida}'.")

# Definições implícitas
#DIRETORIO_BASE = "E:\\Geraldo"  # Altere para o caminho desejado
DIRETORIO_BASE = "F:\\desenv\\Download2024"  # Altere para o caminho desejado

#EXTENSOES = ['.txt', '.py', '.log','.jpg','.jpeg']  # Defina as extensões desejadas
EXTENSOES = ['.pdf']  # Defina as extensões desejadas

ARQUIVO_SAIDA = "resultados-pdf.txt"

# Execução do programa
if __name__ == "__main__":
    buscar_arquivos(DIRETORIO_BASE, EXTENSOES, ARQUIVO_SAIDA)
    
    
