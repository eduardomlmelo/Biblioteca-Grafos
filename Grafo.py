from typing import Optional
from collections import deque
import heapq

# Lista de adjacência
class Graph:

    # Metodo construtor
    def __init__(self, num_vertices: int, weighted: bool = False):
        self.num_vertices = int(num_vertices)
        self.weighted = bool(weighted)
        self.adj_list = {i: [] for i in range(self.num_vertices)} # segue o formato vertice:[(vizinho1, peso1), (vizinho2, peso2), ...]

    # Método privado auxiliar
    def _validar_vertice(self, u: int):
        if not 0 <= u < self.num_vertices:
            raise IndexError(f"O vértice {u} é inválido! Digite um vértice no intervalo de 0 - {self.num_vertices - 1}")

    # Metodo para adicionar aresta ao Grafo
    def add_edge(self, u: int, v: int, weight: float = 1) -> None:
        self._validar_vertice(u)
        self._validar_vertice(v)

        # verifica se está tentando adicionar loops
        if u == v:
            print("os vértices são iguais. Loops não são permitidos")
            return

        # Caso o grafo seja ponderado será atribuido o valor do peso referente a cada aresta
        if not self.weighted:
            weight = 1

        # Verifica se a aresta já existe
        for vizinho, _ in self.adj_list[u]:
            if vizinho == v:
                raise ValueError(f"A aresta {u}-{v} já existe!")

        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))

    # Método para remover aresta do Grafo
    def remove_edge(self, u: int, v: int) -> None:
        self._validar_vertice(u)
        self._validar_vertice(v)

        original_len = len(self.adj_list[u])
        self.adj_list[u] = [(ngb, w) for (ngb, w) in self.adj_list[u] if ngb != v]
        
        if original_len == len(self.adj_list[u]):
            raise ValueError(f"A aresta {u}-{v} não existe para ser removida!")

        self.adj_list[v] = [(ngb, w) for (ngb, w) in self.adj_list[v] if ngb != u]

    # Método para remover vértice do Grafo
    def remove_vertex(self, u: int) -> None:
        self._validar_vertice(u)

        # 1. Remove u da lista de vizinhos dos vizinhos de u
        for vizinho, _ in self.adj_list[u]:
            # CORREÇÃO 1: Usar 'n != u' em vez de 'vizinho != u'
            self.adj_list[vizinho] = [(n, w) for n, w in self.adj_list[vizinho] if n != u]

        # Se for o último, apenas deleta
        if u == self.num_vertices - 1:
            del self.adj_list[u]
            self.num_vertices -= 1
            return
        
        # Lógica de Troca (Swap)
        last_vertice = self.num_vertices - 1
        
        # Copia a lista do último para a posição do u
        self.adj_list[u] = self.adj_list[last_vertice]

        # Atualiza os vizinhos do antigo último para apontarem para u
        for vizinho, peso in self.adj_list[u]:
            novas_arestas = []
            for n, w in self.adj_list[vizinho]:
                if n == last_vertice:
                    # CORREÇÃO 2 e 3: 'append' com 'd' e parênteses duplos para tupla
                    novas_arestas.append((u, w)) 
                else:
                    novas_arestas.append((n, w))
            self.adj_list[vizinho] = novas_arestas

        # Limpa o último
        del self.adj_list[last_vertice]
        self.num_vertices -= 1

    # Metodo para printar a lista de adjacencia do Grafo
    def __str__(self):
        resultado = ""
        for i in range (self.num_vertices):
            resultado += f"{i}: {self.adj_list[i]}\n"
        return resultado

    # Metodo que retorna o número de vértices do grafo.
    def n(self):
        return self.num_vertices

    # Metodo que retorna o número de arestas do grafo.
    def m(self):
        total_arestas = sum(len(self.adj_list[v]) for v in range(self.num_vertices))
        return total_arestas // 2

    # Metodo que retorna a vizinhança do vértice v, ou seja, os vértices adjacentes a v.
    def viz(self, v):
        return [item[0] for item in self.adj_list[v]]

    # Metodo que retorna o grau do vértice v, ou seja, o número de arestas incidentes a v.
    def d(self, v):
        return len(self.adj_list[v])

    # Metodo que retorna o peso da aresta uv.
    def w(self, u: int, v: int) -> Optional[float]:
        try:
            self._validar_vertice(u)
            self._validar_vertice(v)
        except IndexError:
            return None
        
        for vizinho, peso in self.adj_list[u]:
            if vizinho == v:
                return peso

    # Metodo que retorna o menor grau presente no grafo.
    def mind(self):
        menor = self.num_vertices
        for vertice in self.adj_list:
            if menor > len(self.adj_list[vertice]):
                menor = len(self.adj_list[vertice]) 
        return menor
    
    # Metodo que retorna o maior grau presente no grafo.
    def maxd(self):
        maior = 0
        for vertice in self.adj_list:
            if maior < len(self.adj_list[vertice]):
                maior = len(self.adj_list[vertice]) 
        return maior
    
    # Método do algoritmo BFS
    def bfs(self, v: int):
        self._validar_vertice(v)

        d = [float('inf')] * self.num_vertices
        pi = [None] * self.num_vertices

        d[v] = 0
        queue = [v]

        while queue:
            u = queue.pop(0)

            for vizinho, peso in self.adj_list[u]:
                if d[vizinho] == float('inf'):
                    d[vizinho] = d[u] + 1
                    pi[vizinho] = u
                    queue.append(vizinho)

        return d, pi
    
    # Metodo do Algoritmo DFS
    def dfs(self, v: int):
        self._validar_vertice(v)

        # Inicialização das listas
        pi = [None] * self.num_vertices      # Predecessores
        ini = [-1] * self.num_vertices       # Tempo de início (descoberta)
        fim = [-1] * self.num_vertices       # Tempo de fim (término)
        
        # Variável de tempo 
        tempo = [0] 

        # Função interna recursiva 
        def _dfs_visit(u):
            # 1. Marca tempo de descoberta (Cor: Cinza)
            tempo[0] += 1
            ini[u] = tempo[0]
            
            # 2. Visita os vizinhos
            for vizinho, peso in self.adj_list[u]: # Lembre de desempacotar o peso!
                # Se ini for -1, significa que é BRANCO (não visitado)
                if ini[vizinho] == -1:
                    pi[vizinho] = u
                    _dfs_visit(vizinho)
            
            # 3. Marca tempo de término (Cor: Preto)
            tempo[0] += 1
            fim[u] = tempo[0]

        # Chamada inicial
        _dfs_visit(v)
        
        return pi, ini, fim

    
    ''' Falta implementar'''


    # Metodo que Executa o algoritmo de Bellman-Ford a partir do vértice v como origem. Retorna duas listas com os atributos "d" e "pi".
    def bf(self):
        pass

    # Metodo que executa o algoritmo de Dijkstra a partir do vértice v como origem. Retorna duas listas com os atributos "d" e "pi".
    def djikstra(self, v):
        pass

    # Metodo que executa uma coloração própria, buscando minimizar o número de cores através do algoritmo guloso ou outras heurísticas mais sofisticadas.
    def coloracao_propria(self):
        pass    
