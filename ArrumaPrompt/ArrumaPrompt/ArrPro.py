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

    # Divide o texto em quadros individuais
    quadros_texto = [q for q in entrada_quadros.split("Quadro ") if q.strip()]

def processar_quadros(entrada_quadros, personagens):
    log("Iniciando processamento de quadros...")
    quadros = []
    if not entrada_quadros.strip():
        log("Nenhum quadro encontrado no arquivo.")
        return quadros

    # Dividindo o texto em quadros
    quadros_texto = entrada_quadros.split("\n\nQuadro ")
    log(f"Total de quadros identificados: {len(quadros_texto)}")
    for i, quadro_texto in enumerate(quadros_texto, start=1):
        log(f"Processando Quadro {i}...")
        linhas = quadro_texto.strip().split('\n')
        estilo, personagens_quadro, descricao, acao_extra = None, [], None, None

        for linha in linhas:
            log(f"Linha processada: {linha}")
            if linha.startswith('Desenhe o Quadro'):
                partes = linha.split('no estilo')
                if len(partes) > 1:
                    estilo = partes[1].split('.')[0].strip()
                    log(f"Estilo encontrado: {estilo}")
            elif 'Personagens:' in linha:
                nomes_personagens = linha.replace('.', '').split(':')[1].split(',')
                acao_extra = None
                for nome in nomes_personagens:
                    nome_limpo = nome.strip()
                    if nome_limpo in personagens:
                        personagens_quadro.append(personagens[nome_limpo])
                    else:
                        acao_extra = nome_limpo  # Captura ação adicional
                log(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro])}")
            elif linha.startswith('Descrição:') or linha.startswith('Cenário:'):
                descricao = linha.split(':')[1].strip()
                log(f"Descrição/Cenário encontrado: {descricao}")

        if estilo and descricao:
            descricao_completa = f"Desenhe o Quadro {i} no estilo {estilo}.\n{descricao}"
            if acao_extra:
                descricao_completa += f" {acao_extra}"
            descricao_completa += "\n"
            for p in personagens_quadro:
                descricao_completa += f"{p.descricao}\n"
            quadro = Quadro(estilo, descricao, personagens_quadro, descricao_completa)
            quadros.append(quadro)
            log(f"Quadro {i} processado com sucesso.")
        else:
            log(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")
            log(quadro_texto)
            sys.exit(1)

    return quadros

def gerar_saida(quadros):
    saida = ""
    for i, quadro in enumerate(quadros):
        saida += f"{quadro.descricao_completa}"
        if i < len(quadros) - 1:
            saida += "\n"
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

entrada_personagens = ler_arquivo(nome_arquivo_personagens)
entrada_quadros = ler_arquivo(nome_arquivo_quadros)

personagens = processar_personagens(entrada_personagens)
quadros = processar_quadros(entrada_quadros, personagens)
saida = gerar_saida(quadros)
#print("\nSaída Gerada:\n")
#print(saida)
with open("saida.txt", "w") as arquivo_saida:
   arquivo_saida.write(saida)
