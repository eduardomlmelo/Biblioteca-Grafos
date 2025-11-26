from Grafo import *

g = Graph(4, True)
g.add_edge(0, 1, 5)
g.add_edge(0, 2, 2)
g.add_edge(1, 2, 3)
g.add_edge(1, 3, 3)
g.add_edge(3, 0, 4)

print(f"Número de vértices no Grafo: {g.n()}")

print(f"Número de arestas no Grafo: {g.m()}")

print(f"Vértices vizinhos a 1: {g.viz(1)}")

print(f"Grau do vértice 1: {g.d(1)}")

print(f"Peso da aresta (0,3): {g.w(0,3)}")

print(f"Menor grau presente no Grafo: {g.mind()}")

print(f"Maior grau presente no Grafo: {g.maxd()}")

d, pi = g.bfs(3)

print("\n--- Resultado do BFS (Iniciando em 3) ---")
print(f"{'Vértice':<10} | {'Distância (Saltos)':<20} | {'Predecessor (Pai)':<20}")
print("-" * 55)

for i in range(g.n()):
    pai = pi[i] if pi[i] is not None else "Nenhum"
    dist = d[i] if d[i] != float('inf') else "Infinito"
    print(f"{i:<10} | {dist:<20} | {pai:<20}")

pi, ini, fim = g.dfs(2)

# 2. Mostra os resultados de forma formatada
print("\n--- Resultado do DFS (Iniciando em 3) ---")
print(f"{'Vértice':<10} | {'Início (Cinza)':<15} | {'Fim (Preto)':<15} | {'Predecessor':<15}")
print("-" * 65)

for i in range(g.n()):
    pai = pi[i] if pi[i] is not None else "Raíz"
    # ini[i] é o momento que o vértice foi descoberto
    # fim[i] é o momento que terminamos de visitar todos os vizinhos dele
    print(f"{i:<10} | {ini[i]:<15} | {fim[i]:<15} | {pai:<15}")