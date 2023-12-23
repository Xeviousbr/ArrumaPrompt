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

    quadros_texto = entrada_quadros.split("\n\n")
    numero_quadro = 1  # Contador para o número do quadro
    for quadro_texto in quadros_texto:
        linhas = quadro_texto.splitlines()
        estilo, personagens_quadro, descricao, acao_extra = None, [], None, None

        for linha in linhas:
            log(f"{linha}")
            if 'Desenhe o Quadro' in linha:
                partes = linha.split('no estilo')
                if len(partes) > 1:
                    estilo = partes[1].split('.')[0].strip()
                    log(f"Estilo encontrado: {estilo}")
            elif 'Personagens:' in linha:
                nomes_personagens = linha.replace('.', '').split(':')[1].split(',')
                acao_extra = None
                for nome in nomes_personagens:
                    nome = nome.split(",")[0].strip()
                    if nome in personagens:
                        personagens_quadro.append(nome)
                    else:
                        acao_extra = nome  # Captura ação adicional
                log(f"Personagens do quadro: {', '.join(personagens_quadro)}")
            elif 'Descrição:' in linha or 'Cenário:' in linha:
                descricao = linha.split(':')[1].strip()
                log(f"Descrição/Cenário encontrado: {descricao}")

        if estilo and descricao:
            descricao_completa = f"Desenhe o Quadro {numero_quadro} no estilo {estilo}.\n{descricao}"
            if acao_extra and acao_extra.strip():
                descricao_completa += f" {acao_extra.strip()}"
            descricao_completa += "\n"
            for nome_personagem in personagens_quadro:
                descricao_completa += f"{nome_personagem}: {personagens[nome_personagem].descricao}\n"
            quadro = Quadro(estilo, descricao, personagens_quadro, descricao_completa)
            quadros.append(quadro)
            log(f"Quadro {numero_quadro} processado com sucesso.")
        else:
            log(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")
            log(quadro_texto)
            sys.exit(1)

        numero_quadro += 1  # Incrementa o número do quadro para o próximo

    return quadros

def log(mensagem):
    global primeira_chamada_log
    modo = 'w' if primeira_chamada_log else 'a'
    with open("log.txt", modo) as arquivo_log:
        arquivo_log.write(mensagem + "\n")
    primeira_chamada_log = False

def gerar_saida(quadros):
    log("Gerando saída dos quadros processados...")
    saida = ""
    if not quadros:
        log("Nenhum quadro para gerar saída.")
        return saida

    for i, quadro in enumerate(quadros):
        saida += f"{quadro.descricao_completa}\n"
        if quadro.personagens:
            personagens_incluidos = set()  # Conjunto para evitar duplicações
            for nome_personagem in quadro.personagens:
                if nome_personagem not in personagens_incluidos:
                    personagens_incluidos.add(nome_personagem)
                    if nome_personagem in personagens:
                        saida += f"{nome_personagem}: {personagens[nome_personagem].descricao}\n"
                    else:
                        # Inclui descrições adicionais dos personagens que não estão no dicionário
                        saida += f"{nome_personagem}\n"
        if i < len(quadros) - 1:
            saida += "\n"  # Adiciona uma linha em branco entre os quadros

    return saida.rstrip()  # Remove espaços em branco extras no final




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
