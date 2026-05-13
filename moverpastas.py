import shutil
import os

def mover_pasta(origem, destino):
    """
    Move uma pasta de um local para outro, incluindo sub-pastas e arquivos, sobrescrevendo arquivos existentes.

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

        # Move a pasta e todo o seu conteúdo
        for item in os.listdir(origem):
            s = os.path.join(origem, item)
            d = os.path.join(destino, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    # Mescla o conteúdo do diretório
                    mover_pasta(s, d)
                else:
                    shutil.move(s, d)
            else:
                if os.path.exists(d):
                    os.remove(d)
                shutil.move(s, d)

        # Remove a pasta de origem vazia
        os.rmdir(origem)

        print(f"Pasta movida de '{origem}' para '{destino}' com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao mover a pasta: {e}")

# Definições de exemplo
PASTA_ORIGEM = "Z:\\xampp5\\htdocs"  # Altere para o caminho desejado
PASTA_DESTINO = "F:\\desenv\\xamp-veio-note-acer\\xampp5\\htdocs"  # Altere para o caminho desejado
# Execução do programa
mover_pasta(PASTA_ORIGEM, PASTA_DESTINO)

#PASTA_ORIGEM = "Z:\\Users\\Geraldo\\Pictures\\fotos whatsapp antes de agosto 2020"  # Altere para o caminho desejado
#PASTA_DESTINO = "F:\\GERALDO2023\\VEIO-E\\VEIO-ACER\\imagens\\fotos whatsapp antes de agosto 2020"
# Execução do programa
#mover_pasta(PASTA_ORIGEM, PASTA_DESTINO)
