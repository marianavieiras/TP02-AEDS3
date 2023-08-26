import graph
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk


def enviar_dados():
    ano_digitado = entry_ano.get()  # Obtém o valor digitado na caixa de texto
    percentual_digitado = entry_percentual.get()  # Obtém o valor digitado na caixa de texto
    partidos_digitado = entry_partidos.get()  # Obtém o valor digitado na caixa de texto

    gf = graph.Graph()

    gf.ler_arquivo(f'dataset/politicians{ano_digitado}.txt', f'dataset/graph{ano_digitado}.txt', partidos_digitado)
                
    gf.normalizar_pesos()

    gf.plot_heatmap()
    gf.remover_arestas_pouco_significativas(float(percentual_digitado)) 
    gf.plot_centrality()
    gf.inverter_pesos()
    gf.plot_graph()

    root.destroy()

root = tk.Tk()

root.geometry("500x350")
root.resizable(True, True)

label_titulo = tk.Label(root, text="Painel de Configurações")
label_titulo.pack()

label_linha = tk.Label(root, text="") # Pula a linha
label_linha.pack()

label_ano = tk.Label(root, text="Informe o ano a considerar (de 2001 a 2023):")
label_ano.pack()

entry_ano = tk.Entry(root)  # Cria a caixa de texto
entry_ano.pack()

label_linha = tk.Label(root, text="") # Pula a linha
label_linha.pack()

label_percentual = tk.Label(root, text="Informe o percentual mínimo de concordância (threshold) (ex: 0.9):")
label_percentual.pack()

entry_percentual = tk.Entry(root)  # Cria a caixa de texto
entry_percentual.pack()

label_linha = tk.Label(root, text="") # Pula a linha
label_linha.pack()

label_partidos = tk.Label(root, text="Informe os partidos a analisar, separados por espaço (ex: PT MDB PL):")
label_partidos.pack()

entry_partidos = tk.Entry(root)  # Cria a caixa de texto
entry_partidos.pack()

label_linha = tk.Label(root, text="") # Pula a linha
label_linha.pack()

botao = tk.Button(root, text="Enviar Dados", command=enviar_dados)
botao.pack()


resultado_label = tk.Label(root, text="")
resultado_label.pack()

root.mainloop()
