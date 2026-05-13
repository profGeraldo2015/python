import os
import shutil

def mover_arquivos(pasta_origem, pasta_destino, palavra_chave):
    # Criar pasta de destino se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    # Listar todos os arquivos na pasta de origem
    arquivos = os.listdir(pasta_origem)
    
    # Contador de arquivos movidos
    arquivos_movidos = 0
    
    # Procurar arquivos com a palavra-chave
    for arquivo in arquivos:
        if palavra_chave.lower() in arquivo.lower():
            caminho_origem = os.path.join(pasta_origem, arquivo)
            caminho_destino = os.path.join(pasta_destino, arquivo)
            
            # Mover o arquivo
            shutil.move(caminho_origem, caminho_destino)
            arquivos_movidos += 1
            print(f"Arquivo movido: {arquivo}")
    
    print(f"\nTotal de arquivos movidos: {arquivos_movidos}")

# Exemplo de uso
#pasta_origem = "F:/desenv/Download2024"  # Substitua pelo caminho da sua pasta de origem
pasta_origem = "Z:/xampp2/htdocs"  # Substitua pelo caminho da sua pasta de origem

pasta_destino = "F:/desenv/xamp"  # Substitua pelo caminho da sua pasta de destino
#pasta_destino = "F:/desenv/Download2024/BB"  # Substitua pelo caminho da sua pasta de destino

palavra_chave = "zip"  # Substitua pela palavra que você quer procurar

mover_arquivos(pasta_origem, pasta_destino, palavra_chave)
