import re
import sys

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

def processar_quadros(entrada_quadros, personagens):
    print("Iniciando processamento de quadros...")
    quadros = []
    if not entrada_quadros.strip():
        print("Nenhum quadro encontrado no arquivo.")
        return quadros
    quadros_texto = entrada_quadros.split("Quadro ")[1:]  # Divide cada quadro
    for quadro_texto in quadros_texto:
        linhas = quadro_texto.strip().split('\n')
        estilo = None
        personagens_quadro = []
        descricao = None

        for linha in linhas:
            if linha.startswith('Desenhe o Quadro'):
                estilo = linha.split('no estilo')[1].strip().rstrip('.')
                print(f"Estilo encontrado: {estilo}")  # Debug
            elif linha.startswith('Personagens:'):
                nomes_personagens = linha.replace('.', '').split(':')[1].split(',')
                for nome in nomes_personagens:
                    nome = nome.strip()
                    matched_personagens = []
                    for chave, p in personagens.items():
                        nome_personagem = chave.split(",")[0]  # Separando o nome do personagem da descrição
                        print(nome_personagem)  # Debug
                        if nome == nome_personagem:
                            matched_personagens.append(p)
                            print(f"Correspondência encontrada para '{nome}': {p.descricao}")  # Debug
                    if not matched_personagens:
                        print(f"Inconsistência nos personagens: '{nome}' não encontrado.")
                        sys.exit(1)  # Encerra a execução do programa
                    personagens_quadro.extend(matched_personagens)
                print(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro])}")  # Debug
            elif linha.startswith('Descrição:'):
                descricao = linha.split(':')[1].strip()
                print(f"Descrição encontrada: {descricao}")  # Debug

        if estilo and personagens_quadro and descricao:
            quadro = Quadro(estilo, descricao, personagens_quadro)
            quadros.append(quadro)
            print(f"Quadro {estilo} processado com sucesso.")  # Debug
        else:
            print(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")  # Debug

    return quadros

# def processar_quadros(entrada_quadros, personagens):
#     print("Iniciando processamento de quadros...")
#     quadros = []
#     if not entrada_quadros.strip():
#         print("Nenhum quadro encontrado no arquivo.")
#         return quadros
#     quadros_texto = entrada_quadros.split("Quadro ")[1:]  # Divide cada quadro
#     for quadro_texto in quadros_texto:
#         linhas = quadro_texto.strip().split('\n')
#         estilo = None
#         personagens_quadro = []
#         descricao = None

#         for linha in linhas:
#             if linha.startswith('Desenhe o Quadro'):
#                 estilo = linha.split('no estilo')[1].strip().rstrip('.')
#                 print(f"Estilo encontrado: {estilo}")  # Debug
#             elif linha.startswith('Personagens:'):
#                 nomes_personagens = linha.replace('.', '').split(':')[1].split(',')
#                 for nome in nomes_personagens:
#                     nome = nome.strip()
#                     matched_personagens = []
#                     for p in personagens.values():
#                         print(p.descricao.split(":")[0])
#                         if nome in p.descricao.split(":")[0]:
#                             matched_personagens.append(p)
#                             print(f"Correspondência encontrada para '{nome}': {p.descricao}")  # Debug
#                     if not matched_personagens:
#                         print(f"Inconsistência nos personagens: '{nome}' não encontrado.")
#                         sys.exit(1)  # Encerra a execução do programa
#                     personagens_quadro.extend(matched_personagens)
#                 print(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro])}")  # Debug
#             elif linha.startswith('Descrição:'):
#                 descricao = linha.split(':')[1].strip()
#                 print(f"Descrição encontrada: {descricao}")  # Debug
#         if estilo and personagens_quadro and descricao:
#             quadro = Quadro(estilo, descricao, personagens_quadro)
#             quadros.append(quadro)
#             print(f"Quadro {estilo} processado com sucesso.")  # Debug
#         else:
#             print(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")  # Debug

#     return quadros

# Resto do código permanece o mesmo...


# def processar_quadros(entrada_quadros, personagens):
#     print("Iniciando processamento de quadros...")
#     quadros = []
#     if not entrada_quadros.strip():
#         print("Nenhum quadro encontrado no arquivo.")
#         return quadros
#     quadros_texto = entrada_quadros.split("Quadro ")[1:]  # Divide cada quadro
#     for quadro_texto in quadros_texto:
#         linhas = quadro_texto.strip().split('\n')
#         estilo = None
#         personagens_quadro = []
#         descricao = None

#         for linha in linhas:
#             if linha.startswith('Desenhe o Quadro'):
#                 estilo = linha.split('no estilo')[1].strip().rstrip('.')
#                 print(f"Estilo encontrado: {estilo}")  # Debug
#             elif linha.startswith('Personagens:'):
#                 nomes_personagens = linha.replace('.', '').split(':')[1].split(',')
#                 for nome in nomes_personagens:
#                     nome = nome.strip()
#                     matched_personagens = [p for p in personagens.values() if nome in p.descricao.split(",")[0]]
#                     if not matched_personagens:
#                         print(f"Inconsistência nos personagens: '{nome}' não encontrado.")
#                         sys.exit(1)  # Encerra a execução do programa
#                     personagens_quadro.extend(matched_personagens)
#                 print(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro])}")  # Debug
#             elif linha.startswith('Descrição:'):
#                 descricao = linha.split(':')[1].strip()
#                 print(f"Descrição encontrada: {descricao}")  # Debug

#         if estilo and personagens_quadro and descricao:
#             quadro = Quadro(estilo, descricao, personagens_quadro)
#             quadros.append(quadro)
#             print(f"Quadro {estilo} processado com sucesso.")  # Debug
#         else:
#             print(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")  # Debug

#     return quadros


# def processar_quadros(entrada_quadros, personagens):
#     print("Iniciando processamento de quadros...")
#     quadros = []
#     if not entrada_quadros.strip():
#         print("Nenhum quadro encontrado no arquivo.")
#         return quadros
#     quadros_texto = entrada_quadros.split("Quadro ")[1:]  # Divide cada quadro
#     for quadro_texto in quadros_texto:
#         linhas = quadro_texto.strip().split('\n')
#         estilo = None
#         personagens_quadro = []
#         descricao = None

#         for linha in linhas:
#             if linha.startswith('Desenhe o Quadro'):
#                 estilo = linha.split('no estilo')[1].strip().rstrip('.')
#                 print(f"Estilo encontrado: {estilo}")  # Debug
#             elif linha.startswith('Personagens:'):
#                 nomes_personagens = linha.replace('.', '').split(':')[1].split(',')
#                 for nome in nomes_personagens:
#                     nome = nome.strip()
#                     matched_personagens = [p for p in personagens.values() if nome in p.descricao.split(",")[0]]
#                     personagens_quadro.extend(matched_personagens)
#                 if not personagens_quadro:
#                     print(f"Nenhum personagem correspondente encontrado para: {nomes_personagens}")
#                 else:
#                     print(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro])}")  # Debug
#             elif linha.startswith('Descrição:'):
#                 descricao = linha.split(':')[1].strip()
#                 print(f"Descrição encontrada: {descricao}")  # Debug

#         if estilo and personagens_quadro and descricao:
#             quadro = Quadro(estilo, descricao, personagens_quadro)
#             quadros.append(quadro)
#             print(f"Quadro {estilo} processado com sucesso.")  # Debug
#         else:
#             print(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")  # Debug

#     return quadros

# Resto do código permanece o mesmo...


# def processar_quadros(entrada_quadros, personagens):
#     print("Iniciando processamento de quadros...")
#     quadros = []
#     if not entrada_quadros.strip():
#         print("Nenhum quadro encontrado no arquivo.")
#         return quadros
#     quadros_texto = entrada_quadros.split("Quadro ")[1:]  # Divide cada quadro
#     for quadro_texto in quadros_texto:
#         linhas = quadro_texto.strip().split('\n')
#         estilo = None
#         personagens_quadro = []
#         descricao = None

#         for linha in linhas:
#             if linha.startswith('Desenhe o Quadro'):
#                 estilo = linha.split('no estilo')[1].strip().rstrip('.')
#                 print(f"Estilo encontrado: {estilo}")  # Debug
#             elif linha.startswith('Personagens:'):
#                 nomes_personagens = linha.split(':')[1].split(',')
#                 for nome in nomes_personagens:
#                     nome = nome.strip()
#                     matched_personagens = [p for p in personagens.values() if nome in p.descricao.split(",")[0]]
#                     personagens_quadro.extend(matched_personagens)
#                 if not personagens_quadro:
#                     print(f"Nenhum personagem correspondente encontrado para: {nomes_personagens}")
#                 else:
#                     print(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro])}")  # Debug
#             elif linha.startswith('Descrição:'):
#                 descricao = linha.split(':')[1].strip()
#                 print(f"Descrição encontrada: {descricao}")  # Debug

#         if estilo and personagens_quadro and descricao:
#             quadro = Quadro(estilo, descricao, personagens_quadro)
#             quadros.append(quadro)
#             print(f"Quadro {estilo} processado com sucesso.")  # Debug
#         else:
#             print(f"Não foi possível criar o quadro. Estilo: {estilo}, Personagens: {personagens_quadro}, Descrição: {descricao}")  # Debug

#     return quadros

# Resto do código permanece o mesmo...


# def processar_quadros(entrada_quadros, personagens):
#     print("Iniciando processamento de quadros...")
#     quadros = []
#     if not entrada_quadros.strip():
#         print("Nenhum quadro encontrado no arquivo.")
#         return quadros
#     quadros_texto = entrada_quadros.split("Quadro ")[1:]  # Divide cada quadro
#     for quadro_texto in quadros_texto:
#         linhas = quadro_texto.strip().split('\n')
#         estilo = None
#         personagens_quadro = []
#         descricao = None

#         for linha in linhas:
#             if linha.startswith('Desenhe o Quadro'):
#                 estilo = linha.split('no estilo')[1].strip().rstrip('.')
#                 print(f"Estilo encontrado: {estilo}")  # Debug
#             elif linha.startswith('Personagens:'):
#                 nomes_personagens = linha.split(':')[1].split(',')
#                 for nome in nomes_personagens:
#                     nome = nome.strip()
#                     # Busca flexível por correspondência parcial nos nomes dos personagens
#                     matched_personagens = [p for p in personagens.values() if nome in p.descricao]
#                     personagens_quadro.extend(matched_personagens)
#                 print(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro])}")  # Debug
#             elif linha.startswith('Descrição:'):
#                 descricao = linha.split(':')[1].strip()
#                 print(f"Descrição encontrada: {descricao}")  # Debug

#         if estilo and personagens_quadro and descricao:
#             quadro = Quadro(estilo, descricao, personagens_quadro)
#             quadros.append(quadro)
#             print(f"Quadro {estilo} processado com sucesso.")  # Debug
#         else:
#             print("Informações insuficientes para criar um quadro.")  # Debug

#     return quadros

# Resto do código permanece o mesmo...


# def processar_quadros(entrada_quadros, personagens):
#     print("Iniciando processamento de quadros...")
#     quadros = []
#     if not entrada_quadros.strip():
#         print("Nenhum quadro encontrado no arquivo.")
#         return quadros
#     quadros_texto = entrada_quadros.split("Quadro ")[1:]  # Divide cada quadro
#     for quadro_texto in quadros_texto:
#         linhas = quadro_texto.strip().split('\n')
#         estilo = None
#         personagens_quadro = []
#         descricao = None

#         for linha in linhas:
#             if linha.startswith('Desenhe o Quadro'):
#                 estilo = linha.split('no estilo')[1].strip().rstrip('.')
#                 print(f"Estilo encontrado: {estilo}")  # Debug
#             elif linha.startswith('Personagens:'):
#                 nomes_personagens = linha.split(':')[1].split(',')
#                 for nome in nomes_personagens:
#                     nome = nome.strip()
#                     # Encontrar correspondência parcial para o nome do personagem
#                     for chave in personagens.keys():
#                         if nome in chave:
#                             personagens_quadro.append(personagens[chave])
#                             break
#                 print(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro if p])}")  # Debug
#             elif linha.startswith('Descrição:'):
#                 descricao = linha.split(':')[1].strip()
#                 print(f"Descrição encontrada: {descricao}")  # Debug

#         if estilo and personagens_quadro and descricao:
#             quadro = Quadro(estilo, descricao, personagens_quadro)
#             quadros.append(quadro)
#             print(f"Quadro {estilo} processado com sucesso.")  # Debug
#         else:
#             print("Informações insuficientes para criar um quadro.")  # Debug

#     return quadros

# Resto do código permanece o mesmo...


# def processar_quadros(entrada_quadros, personagens):
#     print("Iniciando processamento de quadros...")
#     quadros = []
#     if not entrada_quadros.strip():
#         print("Nenhum quadro encontrado no arquivo.")
#         return quadros
#     quadros_texto = entrada_quadros.split("Quadro ")[1:]  # Divide cada quadro
#     for quadro_texto in quadros_texto:
#         linhas = quadro_texto.strip().split('\n')
#         estilo = None
#         personagens_quadro = []
#         descricao = None

#         for linha in linhas[1:]:  # Ignora a primeira linha que contém "Quadro X:"
#             if linha.startswith('- Desenhe o Quadro'):
#                 estilo = linha.split('no estilo')[1].strip().rstrip('.')
#                 print(f"Estilo encontrado: {estilo}")  # Debug
#             elif linha.startswith('- Personagens:'):
#                 nomes_personagens = linha.split(':')[1].split(',')
#                 personagens_quadro = [personagens.get(nome.strip()) for nome in nomes_personagens if nome.strip() in personagens]
#                 print(f"Personagens do quadro: {', '.join([p.descricao for p in personagens_quadro if p])}")  # Debug
#             elif linha.startswith('- Descrição:'):
#                 descricao = linha.split(':')[1].strip()
#                 print(f"Descrição encontrada: {descricao}")  # Debug

#         if estilo and personagens_quadro and descricao:
#             quadro = Quadro(estilo, descricao, personagens_quadro)
#             quadros.append(quadro)
#             print(f"Quadro {estilo} processado com sucesso.")  # Debug
#         else:
#             print("Informações insuficientes para criar um quadro.")  # Debug

#     return quadros

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
