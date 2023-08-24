import csv
import sys
import requests
import txt
class Graph:
  
  def __init__(self):

    self.grafo = {}
    self.num_vert = 0
    self.arestas = 0

    
  def add_aresta(self, u, v, w=1):
    if(u in self.grafo):
        if (v in self.grafo[u]):
          self.grafo[u][v] += 1
          return
    else:
      self.grafo[u] = {}
    self.grafo[u][v] = w
    self.arestas += 1
    
  #Ler um arquivo csv
  def ler_arquivo(self, arquivo_politicos, arquivo_grafo, partidos_desejados):
    try:
        with open(arquivo_politicos, 'r', encoding='utf-8') as politicos, open(arquivo_grafo, 'r', encoding='utf-8') as grafo:
            politicos_dict = {}
            for linha in politicos:
                nome, partido, num_votos = linha.strip().split(";")
                num_votos = int(num_votos)
                politicos_dict[nome] = partido

            for linha in grafo:
                dep1, dep2, votos = linha.strip().split(";")
                votos = int(votos)
                if votos > 0:
                    partido_dep1 = politicos_dict.get(dep1)
                    partido_dep2 = politicos_dict.get(dep2)
                    if partido_dep1 in partidos_desejados and partido_dep2 in partidos_desejados:
                        self.add_aresta(dep1, dep2, votos)
    except FileNotFoundError:
        print("Não foi possível encontrar ou ler os arquivos. Verifique as entradas.")


    
          
  def normalizar_pesos(self):
     for u, arestas in self.grafo.items():
            for v in arestas:
                votes_u = self.contar_votacoes(u)
                votes_v = self.contar_votacoes(v)
                self.grafo[u][v] = self.grafo[u][v] / min(votes_u, votes_v)
                
  def contar_votacoes(self, deputado):
        total_votacoes = 0
        if deputado in self.grafo:
            arestas = self.grafo[deputado]
            for v in arestas:
                total_votacoes += arestas[v]
        return total_votacoes
      
  def remover_arestas_pouco_significativas(self, threshold):
        arestas_para_remover = []

        for u, arestas in self.grafo.items():
            for v, peso in arestas.items():
                if peso < threshold:
                    arestas_para_remover.append((u, v))

        for u, v in arestas_para_remover:
            del self.grafo[u][v]
            
  def inverter_pesos(self):
        for u, arestas in self.grafo.items():
            for v in arestas:
                self.grafo[u][v] = 1 - self.grafo[u][v]
        

