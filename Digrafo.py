from Grafo import Graph

class Digraph(Graph):

    def __init__(self, weighted = False):
        super().__init__(weighted)



    # Metodo para adicionar aresta ao grafo
    def add_edge(self, u: int, v: int, weight: float = 1) -> None:
        # verifica se está tentando adicionar loops
        if u == v:
            print("os vértices são iguais. Loops não são permitidos")
            return

        self._validar_vertice(u)
        self._validar_vertice(v)
        
        # Caso o grafo seja ponderado será atribuido o valor do peso referente a cada aresta
        if not self.weighted:
            weight = 1

        # Verifica se a aresta já existe
        for vizinho, _ in self.adj_list[u]:
            if vizinho == v:
                raise ValueError(f"A aresta {u}-{v} já existe!")

        self.adj_list[u].append((v, weight))

    # Metodo que retorna o número de arestas do grafo.
    def m(self):
        total_arestas = sum(len(vizinhos) for vizinhos in self.adj_list.values())
        return total_arestas

    ''' Analisar pra tirar a "cara" de chatgpt '''

    # Metodo que retorna a vizinhança do vértice v, ou seja, os vértices adjacentes a v.
    def viz(self, v):
        if v not in self.adj_list:
            print("vértice não existe")
            return

        # out-neighbors
        out_n = [u for u, _ in self.adj_list[v]]

        # in-neighbors
        in_n = []
        for u in self.adj_list:
            for vizinho, _ in self.adj_list[u]:
                if vizinho == v:
                    in_n.append(u)

        return in_n + out_n

    
    # Metodo que retorna o grau do vértice v, ou seja, o número de arestas incidentes a v.
    def d(self, v):
        if v not in self.adj_list:
            print("vértice não existe")
            return

        outd = len(self.adj_list[v])
        ind = sum(1 for u in self.adj_list for viz,_ in self.adj_list[u] if viz == v)

        return ind + outd
