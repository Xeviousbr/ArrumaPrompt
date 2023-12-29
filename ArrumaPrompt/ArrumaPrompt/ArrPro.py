import re
import sys

primeira_chamada_log = True

class Personagem:
    def __init__(self, descricao):
        self.descricao = descricao
        self.seed = descricao.split("Seed: ")[1]
      
class Quadro:
   def __init__(self, estilo, descricao, personagens, descricao_completa):
       self.estilo = estilo
       self.descricao = descricao
       self.personagens = personagens
       self.descricao_completa = descricao_completa

def extrair_personagens_do_quadro(linha, personagens_dict):
    personagens_quadro = {}
    if 'Personagens:' in linha:
        nomes_personagens = linha.split(':')[1].split(',')
        for nome in nomes_personagens:
            nome_limpo = nome.strip()
            if nome_limpo in personagens_dict:
                personagens_quadro[nome_limpo] = personagens_dict[nome_limpo]
    return personagens_quadro

def processar_quadros(entrada_quadros, personagens):
    log("Iniciando processamento de quadros...")
    quadros = []
    if not entrada_quadros.strip():
        log("Nenhum quadro encontrado no arquivo.")
        return quadros

    quadros_texto = entrada_quadros.split("Desenhe o ")[1:]  # Ignora a primeira parte vazia
    log(f"Total de quadros identificados: {len(quadros_texto)}")

    for i, quadro_texto in enumerate(quadros_texto, start=1):
        linhas = quadro_texto.strip().split('\n')
        estilo, personagens_quadro, descricao = None, [], None

        for linha in linhas:
            log(f"Linha processada: {linha}")
            if not estilo:
                log("not estilo")
                estilo = processar_estilo(linha)
            if not personagens_quadro:
                log("not personagens_quadro")
                personagens_quadro = extrair_personagens_do_quadro(linha, personagens)
            if not descricao:
                log("not descricao")
                descricao = processar_descricao(linha)

        if estilo and descricao:
            descricao_completa = f"Desenhe o Quadro {i} no estilo {estilo}\n{descricao}\n"
            for nome, p in personagens_quadro.items():
                descricao_completa += f"{nome}: {p.descricao}\n"
            descricao_completa = descricao_completa.strip() + "\n\n"  # Adiciona uma linha em branco após os personagens e remove espaços extras
            quadro = Quadro(estilo, descricao, personagens_quadro, descricao_completa)
            quadros.append(quadro)
            log(f"Quadro {i} processado com sucesso.")            
        else:
            log(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")
            log(quadro_texto)
            sys.exit(1)

    return quadros  

def processar_estilo(linha):
    if 'no estilo' in linha:
        estilo = linha.split('no estilo')[1].strip()
        return estilo
    return None

def processar_personagens(entrada_personagens):
    personagens = {}
    if not entrada_personagens.strip():
        return personagens
    for linha in entrada_personagens.split('\n'):
        match = re.match(r"([^:]+): (.+)", linha.strip())
        if match:
            nome, descricao = match.groups()
            personagens[nome] = Personagem(descricao)
    return personagens

def processar_descricao(linha):
    if 'Descrição:' in linha:
        descricao = linha.split(':')[1].strip()
        return descricao
    return None

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

def gerar_saida(quadros):
    saida = ""
    for i, quadro in enumerate(quadros):
        saida += f"{quadro.descricao_completa}"
        # if i < len(quadros) - 1:
        #     saida += "\n"
    return saida.rstrip()

def log(mensagem):
    global primeira_chamada_log
    modo = 'w' if primeira_chamada_log else 'a'
    with open("log.txt", modo) as arquivo_log:
        arquivo_log.write(mensagem + "\n")
    primeira_chamada_log = False

def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return ""

nome_arquivo_personagens = 'personagens.txt'
nome_arquivo_quadros = 'quadros.txt'

log("Lendo entradadas")

entrada_personagens = ler_arquivo(nome_arquivo_personagens)
entrada_quadros = ler_arquivo(nome_arquivo_quadros)

log("Entradas lidas")

personagens = processar_personagens(entrada_personagens)
quadros = processar_quadros(entrada_quadros, personagens)
saida = gerar_saida(quadros)
with open("saida.txt", "w") as arquivo_saida:
   arquivo_saida.write(saida)
