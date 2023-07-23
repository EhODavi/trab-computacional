import math
import sys
import time
import networkx as nx
import matplotlib.pyplot as plt


def leitura(conteudo):
    x = []
    y = []

    n = int(conteudo[0])

    for i in range(1, n + 1):
        conteudo_linha = conteudo[i].split()

        x.append(int(conteudo_linha[0]))
        y.append(int(conteudo_linha[1]))

    matriz_distancias = []

    for i in range(n):
        matriz_distancias.append([])

        for j in range(n):
            matriz_distancias[i].append(0)

    distance = lambda x1, y1, x2, y2: int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) + 0.5)

    for i in range(n):
        for j in range(n):
            matriz_distancias[i][j] = distance(x[i], y[i], x[j], y[j])

    return x, y, n, matriz_distancias


def avalia_solucao(solucao, distancias):
    valor_total = 0

    for i in range(len(solucao) - 1):
        valor_total = valor_total + distancias[solucao[i] - 1][solucao[i + 1] - 1]

    return valor_total


def desenhar(solucao, x, y, n):
    G = nx.DiGraph()

    for i in range(1, n + 1):
        G.add_node(i, color='blue', pos=(x[i - 1], y[i - 1]))

    for i in range(len(solucao) - 1):
        G.add_edge(solucao[i], solucao[i + 1], color='blue', weight=1)

    edge_colors = nx.get_edge_attributes(G, 'color').values()
    weights = nx.get_edge_attributes(G, 'weight').values()
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    pos = nx.get_node_attributes(G, 'pos')

    nx.draw(G, pos=pos, edge_color=edge_colors, node_color=colors, font_color='black', width=list(weights), node_size=50)

    plt.show()


def proxima_permutacao(permutacao):
    for i in reversed(range(len(permutacao) - 1)):
        if permutacao[i] < permutacao[i + 1]:
            break
    else:
        return False

    j = next(j for j in reversed(range(i + 1, len(permutacao))) if permutacao[i] < permutacao[j])

    permutacao[i], permutacao[j] = permutacao[j], permutacao[i]

    permutacao[i + 1:] = reversed(permutacao[i + 1:])

    return True


def main():
    inicio = time.time()

    if len(sys.argv) != 2:
        print("Erro, use: python questao-1.py arquivo")
        exit(-1)

    arquivo = open(sys.argv[1], 'r')
    conteudo_arquivo = []

    for linha in arquivo:
        linha = linha.strip()
        conteudo_arquivo.append(linha)

    x, y, n, distancias = leitura(conteudo_arquivo)

    permutacao = []

    for i in range(2, n + 1):
        permutacao.append(i)

    melhor_permutacao = permutacao.copy()

    melhor_permutacao.insert(0, 1)
    melhor_permutacao.append(1)

    menor_avaliacao = avalia_solucao(melhor_permutacao, distancias)

    i = 1

    while proxima_permutacao(permutacao):
        prox_permutacao = permutacao.copy()

        prox_permutacao.insert(0, 1)
        prox_permutacao.append(1)

        avaliacao = avalia_solucao(prox_permutacao, distancias)

        if avaliacao < menor_avaliacao:
            menor_avaliacao = avaliacao
            melhor_permutacao = prox_permutacao.copy()

        i = i + 1

        fim = time.time()

        if fim - inicio >= 7200:
            break

    print(f"{melhor_permutacao} = {menor_avaliacao}")
    print(f"Num. Ciclos Gerados = {i}")

    print(fim - inicio)

    desenhar(melhor_permutacao, x, y, n)

    arquivo.close()


if __name__ == "__main__":
    main()
