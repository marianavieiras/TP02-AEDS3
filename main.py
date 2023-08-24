import graph
import csv
import networkx as nx
import matplotlib.pyplot as plt


ano = int(input("Informe o ano você deseja tratar os seus dados: "))

gf = graph.Graph() 

partidos_filtrados = input("Informe os partidos separados por espaço (ou pressione Enter para não filtrar): ").split(" ")

gf.ler_arquivo(f'dataset/politicians{ano}.txt', f'dataset/graph{ano}.txt', partidos_filtrados)
print("Arestas no grafo:")
for u, arestas in gf.grafo.items():
    for v, peso in arestas.items():
        print(f"{u} -> {v}: {peso}")
            
gf.normalizar_pesos()
gf.remover_arestas_pouco_significativas(0.5) 
gf.inverter_pesos()

