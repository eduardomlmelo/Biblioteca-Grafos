from typing import Optional
from collections import deque
import heapq

# Lista de adjacência
class Graph:

    # Metodo construtor
    def __init__(self, weighted: bool = False):
        self.weighted = bool(weighted)
        self.adj_list = {} # segue o formato vertice:[(vizinho1, peso1), (vizinho2, peso2), ...]
    
    """ Métodos Auxiliares """

    # Metodo para printar a lista de adjacencia do Grafo
    def __str__(self):
        resultado = ""
        for i in range (self.n):
            resultado += f"{i}: {self.adj_list[i]}\n"
        return resultado
    
    # Método privado auxiliar
    def _validar_vertice(self, u: str):
        if u not in self.adj_list:
            self.adj_list[u] = [] # se o vértice não existe na lista de adjacência, então cria um "elemento" para ele

    # Metodo para adicionar aresta ao Grafo
    def add_edge(self, u: str, v: str, weight: int = 1) -> None:
        # verifica se está tentando adicionar loops
        if u == v:
            print("os vértices são iguais. Loops não são permitidos")
            return

        self._validar_vertice(u)
        self._validar_vertice(v)
        
        # Caso o grafo seja ponderado será atribuido o valor do peso referente a cada aresta
        if not self.weighted:
            weight = 1
            
        self.adj_list[u].append((v, weight))
        self.adj_list[v].append((u, weight))

    # Método para remover vértice do Grafo
    def remove_vertex(self, u: str) -> None:
        if u not in self.adj_list:
            print("vértice não existe \n")
            return
        
        ''' implementação 1'''
        # Percorre todos os vizinhos desse vértice
        for vizinho, _ in self.adj_list[u]:
            # refaz a lista do "vizinho" sem o vértice "u"
            self.adj_list[vizinho] = [(v, w) for v, w in self.adj_list[vizinho] if v != u]
        
        # apaga o vértice "u"
        del self.adj_list[u]
        

    '''
    # Método para remover aresta do Grafo
    def remove_edge(self, u: int, v: int) -> None:
        self._validar_vertice(u)
        self._validar_vertice(v)

        original_len = len(self.adj_list[u])
        self.adj_list[u] = [(ngb, w) for (ngb, w) in self.adj_list[u] if ngb != v]
        
        if original_len == len(self.adj_list[u]):
            raise ValueError(f"A aresta {u}-{v} não existe para ser removida!")

        self.adj_list[v] = [(ngb, w) for (ngb, w) in self.adj_list[v] if ngb != u]
    '''  
   

    """ Métodos Úteis """

    # Metodo que retorna o número de vértices do grafo.
    def n(self):
        return len(self.adj_list)

    # Metodo que retorna o número de arestas do grafo.
    def m(self):
        total_arestas = sum(len(vizinhos) for vizinhos in self.adj_list.values())
        return total_arestas // 2

    # Metodo que retorna a vizinhança do vértice v, ou seja, os vértices adjacentes a v.
    def viz(self, v: str):
        if v not in self.adj_list:
            print("vértice não existe \n")
            return
        
        return [vizinho for vizinho, _ in self.adj_list[v]]

    # Metodo que retorna o grau do vértice v, ou seja, o número de arestas incidentes a v.
    def d(self, v: str):
        if v not in self.adj_list:
            print("vértice não existe \n")
            return
        
        return len(self.adj_list[v])

    # Metodo que retorna o peso da aresta uv.
    def w(self, u: str, v: str) -> Optional[float]:
        if u not in self.adj_list or v not in self.adj_list:
            print("a aresta não existe \n")
            return
        
        for vizinho, peso in self.adj_list[u]:

            if vizinho == v:
                return peso

    # Metodo que retorna o menor grau presente no grafo.
    def mind(self):
        # lista vazia
        if not self.adj_list:
            return 0

        menor = float('inf')

        for vizinhos in self.adj_list.values():
            grau = len(vizinhos)

            if grau < menor:
                menor = grau

        return menor 
    
    # Metodo que retorna o maior grau presente no grafo.
    def maxd(self):
        # lista vazia
        if not self.adj_list:
            return 0
        
        maior = 0
        
        for vizinhos in self.adj_list.values():
            grau = len(vizinhos)

            if grau > maior:
                maior = grau

        return grau


    """ Algoritmos """

    # Método do algoritmo BFS
    def bfs(self, v: str):
        if v not in self.adj_list:
            print("vértice não existe \n")
            return

        d = {vertice:float('inf') for vertice in self.adj_list.keys()} # no formato -> vertice:dist_ate_v
        pi = {vertice:None for vertice in self.adj_list.keys()} # no formato -> vertice:predecessor


        d[v] = 0
        queue = deque([v])

        while queue:
            u = queue.popleft()

            for vizinho, _ in self.adj_list[u]:

                if d[vizinho] == float('inf'):
                    d[vizinho] = d[u] + 1
                    pi[vizinho] = u

                    queue.append(vizinho)
            
        return d, pi
    
    # Metodo do Algoritmo DFS
    def dfs(self, v: str):
        if v not in self.adj_list:
            print("vértice não existe \n")
            return

        # Inicialização das listas
        pi = {vertice:None for vertice in self.adj_list.keys()} # no formato -> vertice:predecessor
        ini = {vertice:-1 for vertice in self.adj_list.keys()} # no formato -> vertice:tempo_chegada
        fim = {vertice:-1 for vertice in self.adj_list.keys()} # no formato -> vertice:tempo_saida
 
        tempo = [0]

        def _dfs_visit(u):

            tempo[0] += 1
            ini[u] = tempo[0]

            for vizinho, _ in self.adj_list[u]:

                if ini[vizinho] == -1:
                    pi[vizinho] = u
                    _dfs_visit(vizinho)

            tempo[0] += 1
            fim[u] = tempo[0]

        _dfs_visit(v)

        return pi, ini, fim

    # Metodo que executa o algoritmo de Dijkstra a partir do vértice v como origem. Retorna duas listas com os atributos "d" e "pi".
    def djikstra(self, v: str):

        d = {vertice:float('inf') for vertice in self.adj_list.keys()} # no formato -> vertice:dist_ate_v
        pi = {vertice:None for vertice in self.adj_list.keys()} # no formato -> vertice:predecessor

        d[v] = 0

        queue = []
        heapq.heappush(queue, (0, v))

        while queue:

            dist_u, u = heapq.heappop(queue)

            if dist_u > d[u]:
                continue

            for vizinho, peso in self.adj_list[u]: # self.adj_list segue o formato -> vertice:[(vizinho1, peso1), (vizinho2, peso2), ...]
                if d[u] + peso < d[vizinho]:
                    d[vizinho] = d[u] + peso
                    pi[vizinho] = u
                    heapq.heappush(queue, (d[vizinho], vizinho))

        return d, pi

        
    # Metodo que Executa o algoritmo de Bellman-Ford a partir do vértice v como origem. Retorna duas listas com os atributos "d" e "pi".
    def bf(self, v: str):

        ''' pode ser otimizado '''

        d = {vertice:float('inf') for vertice in self.adj_list.keys()} # no formato -> vertice:dist_ate_v
        pi = {vertice:None for vertice in self.adj_list.keys()} # no formato -> vertice:predecessor

        d[v] = 0

        num_vertices = self.n() # retorna o número de vértice do grafo

        for i in range(num_vertices - 1):
            
            for vertice in self.adj_list.keys():

                # itera todos os vizinhos do vértice iterado
                for vizinho, peso in self.adj_list[vertice]: # o grafo é uma lista de adjacência que segue o formato -> vértice:[(vizinho1, peso1), (vizinho2, peso2), ...]

                    if d[vertice] + peso < d[vizinho]:
                        d[vizinho] = d[vertice] + peso
                        pi[vizinho] = vertice

        # verifica se tem ciclos negativos
        for vertice in self.adj_list.keys():

            for vizinho, peso in self.adj_list[vertice]:
                
                if d[vertice] + peso < d[vizinho]:
                    return "CICLO_NEGATIVO_DETECTADO"

        return d, pi


    ''' Falta implementar '''

    # Metodo que executa uma coloração própria, buscando minimizar o número de cores através do algoritmo guloso ou outras heurísticas mais sofisticadas.
    def coloracao_propria(self):
        pass    
