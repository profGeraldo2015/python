import shutil
import os

def copiar_pasta(origem, destino):
    """
    Copia uma pasta de um local para outro, incluindo sub-pastas e arquivos, sobrescrevendo arquivos existentes.

    :param origem: Caminho da pasta de origem.
    :param destino: Caminho da pasta de destino.
    """
    try:
        # Verifica se a pasta de origem existe
        if not os.path.exists(origem):
            print(f"A pasta de origem '{origem}' não existe.")
            return

        # Verifica se a pasta de destino existe, se não, cria
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Copia a pasta e todo o seu conteúdo
        for item in os.listdir(origem):
            s = os.path.join(origem, item)
            d = os.path.join(destino, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    # Mescla o conteúdo do diretório
                    copiar_pasta(s, d)
                else:
                    shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        print(f"Pasta copiada de '{origem}' para '{destino}' com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao copiar a pasta: {e}")

# Definições de exemplo
#PASTA_ORIGEM = "Z:\\Geraldo\\desenv"
PASTA_ORIGEM = "Z:\\Program Files (x86)\\Watchtower"

#PASTA_DESTINO = "F:\\GERALDO2023\\VEIO-E\\VEIO-ACER\\backup-desenv\\desenv"
PASTA_DESTINO = "F:\\GERALDO2023\\Watchtower"

# Execução do programa
copiar_pasta(PASTA_ORIGEM, PASTA_DESTINO)