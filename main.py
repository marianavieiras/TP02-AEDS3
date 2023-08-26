import graph
import networkx as nx
import matplotlib.pyplot as plt


ano = 2023

gf = graph.Graph() 

partidos_filtrados = "PT PSOL"

gf.ler_arquivo(f'dataset/politicians{ano}.txt', f'dataset/graph{ano}.txt', partidos_filtrados)
         
gf.normalizar_pesos()

gf.plot_heatmap()
gf.remover_arestas_pouco_significativas(0.9) 
gf.plot_centrality()
# gf.inverter_pesos()
gf.plot_graph()
