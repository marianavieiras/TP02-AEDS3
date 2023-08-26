import matplotlib.pyplot as plt
import networkx as nx 
import numpy as np 
import random

class Graph:
  
  def __init__(self):
    self.votacoes=[]
    self.grafo = {}
    self.num_vert = 0
    self.arestas = 0
    self.politico_dict = {}
    self.lista = {}    
    
  def add_aresta(self, u, v, w=1):
    if(u in self.grafo):
        if (v in self.grafo[u]):
          self.grafo[u][v] += 1
          self.lista[u] += 1
          return
    else:
      self.grafo[u] = {}
    self.grafo[u][v] = w
    self.lista[u] = w
    self.arestas += 1
    
  #Ler um arquivo csv
  def ler_arquivo(self, arquivo_politicos, arquivo_grafo, partidos_desejados):
    politicos_dict={}
    try:
        with open(arquivo_politicos, 'r', encoding='utf-8') as politicos, open(arquivo_grafo, 'r', encoding='utf-8') as grafo:
            for linha in politicos:
                nome, partido, num_votos = linha.strip().split(";")
                num_votos = int(num_votos)
                tupla = (nome,num_votos)
                politicos_dict[nome] = partido
                self.votacoes.append(tupla)

            for linha in grafo:
                dep1, dep2, votos = linha.strip().split(";")
                votos = int(votos)
                if votos > 0:
                    partido_dep1 = politicos_dict.get(dep1)
                    partido_dep2 = politicos_dict.get(dep2)
                    if partido_dep1 in partidos_desejados and partido_dep2 in partidos_desejados:
                      self.add_aresta(dep1, dep2, votos)
                      self.politico_dict[dep1] = partido_dep1
    except FileNotFoundError:
        print("Não foi possível encontrar ou ler os arquivos. Verifique as entradas.")

          
  def normalizar_pesos(self):
    cont=0
    for u, arestas in self.grafo.items():
        for v in arestas:
            votes_u = self.contar_votacoes(u)
            votes_v = self.contar_votacoes(v)
            normalization_factor = min(votes_u, votes_v)
            w = self.grafo[u][v]
            normalization = w/normalization_factor
            cont+=1
            self.grafo[u][v] = normalization 
  def contar_votacoes(self, nome):  
    for (nomeD,votus) in self.votacoes:
      if nomeD == nome:
        votos = votus
    return votos

  def remover_arestas_pouco_significativas(self, threshold):
      arestas_para_remover = []

      for u, arestas in self.grafo.items():
          for v, peso in arestas.items():
              if peso < threshold:
                  arestas_para_remover.append((u, v))
                  
      for u, v in arestas_para_remover:
          del self.grafo[u][v]
          self.lista[u] -=1
      
      for u in self.lista:
        if self.lista[u] == 0:
          del self.politico_dict[u]    
     
  def remover_vertices_sem_arestas(self):
    vertices_sem_arestas = [v for v in self.grafo if len(self.grafo[v]) == 0]

    for v in vertices_sem_arestas:
        del self.grafo[v]
        if v in self.politico_dict:
          del self.politico_dict[v]   


            
  def inverter_pesos(self):
        for u, arestas in self.grafo.items():
            for v in arestas:
                self.grafo[u][v] = 1 - self.grafo[u][v]
  

  def plot_centrality(self):
    nx_graph = nx.Graph(self.grafo)

    # Centralidade Métrica e Gráfico de Centralidade - Calcular a centralidade de betweenness
    centralidade = nx.betweenness_centrality(nx_graph)
    centralidade = sorted(centralidade.items(), key=lambda x: x[1])
    keys, values = zip(*centralidade)
    plt.figure(figsize=(10, 6))
    plt.title('Centralidade dos Deputados')
    plt.bar(keys, values, align='center')
    plt.xticks(rotation=45, ha="right", fontsize=6)
    plt.xlabel('Deputados')
    plt.ylabel('Centralidade')
    plt.tight_layout()
    
    plt.savefig('centralidade.png')  # Salvar o gráfico como imagem
    
    plt.show()  # Mostrar o gráfico
    
    return None  # Retornar None ou outro valor, se necessário
  
  
  
  
  def plot_heatmap(self):

    deputados = list(self.grafo.keys())
    correlacao = np.zeros((len(deputados), len(deputados)))
    for i, dep1 in enumerate(deputados):
        for j, dep2 in enumerate(deputados):
            if i == j:
                correlacao[i, j] = 1
            else:
                if dep2 in self.grafo[dep1]:
                    correlacao[i, j] = self.grafo[dep1][dep2]


    deputados_labels = deputados

    plt.figure(figsize=(10, 10))
    plt.title('Correlação entre Deputados')
    plt.imshow(correlacao, cmap='hot', interpolation='none', aspect='auto')
    plt.xticks(range(len(deputados)), deputados_labels, rotation=45, ha="right", fontsize=6)
    plt.yticks(range(len(deputados)), deputados_labels, fontsize=6)
    plt.colorbar(label='Nível de Correlação')
    plt.tight_layout()

    plt.savefig('heatmap.png')  # Salvar o heatmap como imagem
    
    plt.show()  # Mostrar o heatmap
    
    return None

    
  def plot_graph(self):
      self.remover_vertices_sem_arestas()
      nx_graph = nx.Graph(self.grafo)

      # Colore o grafo de acordo com o partido de cada deputado
      color_map = {}
      node_colors = []
      for n in nx_graph.nodes():
          if self.politico_dict[n] not in color_map:
              color_map[self.politico_dict[n]] = tuple()
          while len(color_map[self.politico_dict[n]]) == 0:
              color = (random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255)
              if color not in list(color_map.values()):
                  color_map[self.politico_dict[n]] = color
          node_colors.append(color_map[self.politico_dict[n]])
      color_map = dict(sorted(color_map.items()))

      # Plota o grafo
      plt.figure(figsize=(10, 10))
      plt.title('Relações entre Deputados')
      positions = nx.spring_layout(nx_graph)
      nx.draw(nx_graph, positions, node_size=100, node_color=node_colors, width=1, with_labels=True, font_size=10)
      for party, color in color_map.items():
          plt.scatter([], [], c=[color], label=party)
      plt.legend()
      plt.tight_layout()
      plt.show()
      return None




  