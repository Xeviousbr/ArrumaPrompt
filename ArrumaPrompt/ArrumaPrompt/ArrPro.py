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
    personagens = {}
    for linha in entrada_personagens.split('\n'):
        if linha.strip():
            nome, descricao = linha.split(': ', 1)
            personagens[nome] = Personagem(descricao)
    return personagens

def processar_quadros(entrada_quadros, personagens):
    quadros = []
    for quadro_texto in entrada_quadros.split("Quadro ")[1:]:
        partes = quadro_texto.split('\n')
        num_quadro = partes[0].strip()
        estilo = partes[1].replace('Desenhe o Quadro', '').strip()
        personagens_quadro = partes[3].replace('Personagens:', '').split(', ')
        descricao = partes[4].replace('Descrição:', '').strip()
        quadros.append(Quadro(estilo, descricao, [personagens[nome.strip()] for nome in personagens_quadro]))
    return quadros

def gerar_saida(quadros):
    saida = ""
    for quadro in quadros:
        saida += f"Quadro {quadro.estilo}\n"
        saida += f"{quadro.descricao}\n"
        for personagem in quadro.personagens:
            saida += f"{personagem.descricao}\n"
    return saida

# Programa Principal
entrada_personagens = input("Digite as informações dos personagens (separe cada personagem com uma nova linha):\n")
entrada_quadros = input("\nDigite as informações dos quadros (separe cada quadro com 'Quadro [número]'):\n")

personagens = processar_personagens(entrada_personagens)
quadros = processar_quadros(entrada_quadros, personagens)
saida = gerar_saida(quadros)
print("\nSaída Gerada:\n")
print(saida)
