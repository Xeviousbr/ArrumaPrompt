import re
import sys

primeira_chamada_log = True

class Personagem:
    def __init__(self, descricao):
        self.descricao = descricao
        self.seed = descricao.split("Seed: ")[1]

class Quadro:
    def __init__(self, estilo, descricao, personagens):
        self.estilo = estilo
        self.descricao = descricao
        self.personagens = personagens

def processar_personagens(entrada_personagens):
    print("Iniciando processamento de personagens...")
    personagens = {}
    if not entrada_personagens.strip():
        print("Nenhum personagem encontrado no arquivo.")
        return personagens
    for linha in entrada_personagens.split('\n'):
        if linha.strip():
            match = re.match(r"([^:]+): (.+)", linha.strip())
            if match:
                nome, descricao = match.groups()
                personagens[nome] = Personagem(descricao)
                print(f"Processado personagem: {nome}")  # Debug
    return personagens

def encontrar_personagens(nomes_personagens, personagens):
    personagens_encontrados = []
    for nome in nomes_personagens:
        nome = nome.strip()
        correspondencia_encontrada = False
        for chave, p in personagens.items():
            nome_personagem = chave.split(",")[0].strip()
            log(f"Comparando '{nome}' com '{nome_personagem}'")  # Debug
            if nome == nome_personagem:
                personagens_encontrados.append(p)
                correspondencia_encontrada = True
                log(f"Correspondência encontrada para '{nome}': {p.descricao}")  # Debug
                break  # Pára a busca assim que encontrar uma correspondência
        if not correspondencia_encontrada:
            log(f"Inconsistência nos personagens: '{nome}' não encontrado.")
            sys.exit(1)
    return personagens_encontrados

def processar_quadros(entrada_quadros, personagens):
    log("Iniciando processamento de quadros...")
    quadros = []
    if not entrada_quadros.strip():
        log("Nenhum quadro encontrado no arquivo.")
        return quadros
    quadros_texto = entrada_quadros.split("Quadro ")[1:]  # Divide cada quadro
    for quadro_texto in quadros_texto:
        linhas = quadro_texto.split('\n')
        estilo, personagens_quadro, descricao = None, [], None
        contador = 0  # Inicializa um contador para pular a primeira linha

        for linha in linhas:
            if contador == 0:  # Pula a primeira linha (ex.: "Quadro 1")
                contador += 1
                continue

            log(f" {linha}")  # Log de depuração
            if 'Desenhe o Quadro' in linha:
                log(f"Desenhe o Quadro")
                partes = linha.split('no estilo')
                if len(partes) > 1:
                    estilo = partes[1].split('.')[0].strip()
                    log(f"Estilo encontrado: {estilo}")
            elif 'Personagens:' in linha:
                log(f"Personagens")
                nomes_personagens = linha.replace('.', '').split(':')[1].split(',')
                personagens_quadro = encontrar_personagens(nomes_personagens, personagens)
                log(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro])}")
            elif 'Descrição:' in linha:
                log(f"Descrição")
                descricao = linha.split(':')[1].strip()
                log(f"Descrição encontrada: {descricao}")

            contador += 1

        if estilo and personagens_quadro and descricao:
            quadro = Quadro(estilo, descricao, personagens_quadro)
            quadros.append(quadro)
            log(f"Quadro {estilo} processado com sucesso.")
        else:
            log(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")
            log(quadro_texto)
            sys.exit(1)

    return quadros

def log(mensagem):
    global primeira_chamada_log
    modo = 'w' if primeira_chamada_log else 'a'
    with open("log.txt", modo) as arquivo_log:
        arquivo_log.write(mensagem + "\n")
    primeira_chamada_log = False
    
def gerar_saida(quadros):
    print("Gerando saída dos quadros processados...")
    saida = ""
    if not quadros:
        print("Nenhum quadro para gerar saída.")
        return saida

    for quadro in quadros:
        saida += f"Quadro {quadro.estilo}\n"
        saida += f"{quadro.descricao}\n"
        if not quadro.personagens:
            print("Nenhum personagem encontrado para este quadro.")
        for personagem in quadro.personagens:
            if personagem:
                saida += f"{personagem.descricao}\n"
            else:
                print("Personagem não encontrado ou inválido.")
        print(f"Saida parcial: \n{saida}")  # Debug

    return saida

# Resto do código permanece o mesmo...


# def gerar_saida(quadros):
#     saida = ""
#     for quadro in quadros:
#         saida += f"Quadro {quadro.estilo}\n"
#         saida += f"{quadro.descricao}\n"
#         for personagem in quadro.personagens:
#             saida += f"{personagem.descricao}\n"
#     return saida

def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return ""

# Programa Principal
nome_arquivo_personagens = 'personagens.txt'
nome_arquivo_quadros = 'quadros.txt'

entrada_personagens = ler_arquivo(nome_arquivo_personagens)
entrada_quadros = ler_arquivo(nome_arquivo_quadros)

personagens = processar_personagens(entrada_personagens)
quadros = processar_quadros(entrada_quadros, personagens)
saida = gerar_saida(quadros)
print("\nSaída Gerada:\n")
print(saida)
