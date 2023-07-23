import math
import sys
import time
import networkx as nx
import matplotlib.pyplot as plt

from dataclasses import dataclass


@dataclass
class Ponto:
    id: int
    x: int
    y: int


@dataclass
class Reta:
    p: Ponto
    q: Ponto
    a: int
    b: int
    c: int


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

    pontos = []

    for i in range(n):
        p = Ponto(i + 1, x[i], y[i])

        pontos.append(p)

    return matriz_distancias, pontos, n


def avalia_solucao(E, distancias):
    valor_total = 0

    for i in range(len(E) - 1):
        valor_total = valor_total + distancias[E[i] - 1][E[i + 1] - 1]

    return valor_total


def desenhar(E, pontos, n):
    G = nx.DiGraph()

    for i in range(n):
        G.add_node(pontos[i].id, color='blue', pos=(pontos[i].x, pontos[i].y))

    for i in range(len(E) - 1):
        G.add_edge(E[i], E[i + 1], color='blue', weight=1)

    edge_colors = nx.get_edge_attributes(G, 'color').values()
    weights = nx.get_edge_attributes(G, 'weight').values()
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    pos = nx.get_node_attributes(G, 'pos')

    nx.draw(G, pos=pos, edge_color=edge_colors, node_color=colors, font_color='black', width=list(weights), node_size=0.5)

    plt.show()


def poligono_convexo(pa_pb, S1, lado):
    if len(S1) == 0:
        return []
    else:
        p_max = S1[0]
        p_max_distancia = abs(pa_pb.a * p_max.x + pa_pb.b * p_max.y + pa_pb.c) / math.sqrt(math.pow(pa_pb.a, 2) + math.pow(pa_pb.b, 2))

        for s in S1:
            distancia = abs(pa_pb.a * s.x + pa_pb.b * s.y + pa_pb.c) / math.sqrt(math.pow(pa_pb.a, 2) + math.pow(pa_pb.b, 2))

            if distancia > p_max_distancia:
                p_max = s
                p_max_distancia = distancia

        pa_pmax = Reta(pa_pb.p, p_max, p_max.y - pa_pb.p.y, pa_pb.p.x - p_max.x, -(pa_pb.p.x * p_max.y - pa_pb.p.y * p_max.x))

        S11 = []

        for s in S1:
            determinante = pa_pb.p.x * p_max.y + s.x * pa_pb.p.y + p_max.x * s.y - s.x * p_max.y - p_max.x * pa_pb.p.y - pa_pb.p.x * s.y

            if lado == 'esquerdo':
                if determinante > 0:
                    S11.append(s)
            else:
                if determinante < 0:
                    S11.append(s)

        pb_pmax = Reta(pa_pb.q, p_max, p_max.y - pa_pb.q.y, pa_pb.q.x - p_max.x, -(pa_pb.q.x * p_max.y - pa_pb.q.y * p_max.x))

        S22 = []

        for s in S1:
            determinante = pa_pb.q.x * p_max.y + s.x * pa_pb.q.y + p_max.x * s.y - s.x * p_max.y - p_max.x * pa_pb.q.y - pa_pb.q.x * s.y

            if lado == 'esquerdo':
                if determinante < 0:
                    S22.append(s)
            else:
                if determinante > 0:
                    S22.append(s)

        if lado == 'esquerdo':
            pol1 = poligono_convexo(pa_pmax, S11, 'esquerdo')
            pol2 = poligono_convexo(pb_pmax, S22, 'direito')
        else:
            pol1 = poligono_convexo(pa_pmax, S11, 'direito')
            pol2 = poligono_convexo(pb_pmax, S22, 'esquerdo')

        solucao = [p_max]

        for p in pol1:
            inserir = True

            for sol in solucao:
                if p.id == sol.id:
                    inserir = False
                    break

            if inserir:
                solucao.append(p)

        for q in pol2:
            inserir = True

            for sol in solucao:
                if q.id == sol.id:
                    inserir = False
                    break

            if inserir:
                solucao.append(q)

        return solucao


def algoritmo_quick(S, n):
    if n >= 2:
        pa = S[0]
        pb = S[0]

        for s in S:
            if s.x < pa.x:
                pa = s

            if s.x > pb.x:
                pb = s

        EC = [pa, pb]

        pa_pb = Reta(pa, pb, pb.y - pa.y, pa.x - pb.x, -(pa.x * pb.y - pa.y * pb.x))

        S1 = []
        S2 = []

        for s in S:
            if s.id != pa.id and s.id != pb.id:
                if (pa.x * pb.y + s.x * pa.y + pb.x * s.y - s.x * pb.y - pb.x * pa.y - pa.x * s.y) > 0:
                    S1.append(s)
                elif (pa.x * pb.y + s.x * pa.y + pb.x * s.y - s.x * pb.y - pb.x * pa.y - pa.x * s.y) < 0:
                    S2.append(s)

        EC1 = poligono_convexo(pa_pb, S1, 'esquerdo')
        EC2 = poligono_convexo(pa_pb, S2, 'direito')

        return EC, EC1, EC2


def main():
    inicio = time.time()

    if len(sys.argv) != 2:
        print("Erro, use: python questao-3.py arquivo")
        exit(-1)

    arquivo = open(sys.argv[1], 'r')
    conteudo_arquivo = []

    for linha in arquivo:
        linha = linha.strip()
        conteudo_arquivo.append(linha)

    distancias, pontos, n = leitura(conteudo_arquivo)

    EC, EC1, EC2 = algoritmo_quick(pontos, n)

    EC1.sort(key=lambda ponto: ponto.x)
    EC2.sort(key=lambda ponto: ponto.x)

    E = []
    N = []

    E.append(EC[0].id)

    for ec1 in EC1:
        E.append(ec1.id)

    E.append(EC[1].id)

    for i in range(len(EC2) - 1, -1, -1):
        E.append(EC2[i].id)

    E.append(EC[0].id)

    for ponto in pontos:
        inserir = True

        for e in E:
            if ponto.id == e:
                inserir = False
                break

        if inserir:
            N.append(ponto.id)

    N.sort()

    while len(N) >= 1:
        menor_distancia = None

        for i in range(1, len(E)):
            for j in range(len(N)):
                d = distancias[E[i - 1] - 1][N[j] - 1] + distancias[N[j] - 1][E[i] - 1] - distancias[E[i - 1] - 1][E[i] - 1]

                if menor_distancia is None:
                    melhor_indice = i
                    menor_distancia = d
                    melhor_elemento = N[j]
                elif d < menor_distancia:
                    melhor_indice = i
                    menor_distancia = d
                    melhor_elemento = N[j]

        E.insert(melhor_indice, melhor_elemento)
        N.remove(melhor_elemento)

    print(f"{E} = {avalia_solucao(E, distancias)}")

    fim = time.time()

    print(fim - inicio)

    desenhar(E, pontos, n)

    arquivo.close()


if __name__ == "__main__":
    main()
