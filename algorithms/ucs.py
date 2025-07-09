# -*- coding: utf-8 -*-

# Importa a biblioteca 'heapq' para implementar uma Fila de Prioridade.
import heapq
# Importa tipos para anotações.
from typing import Optional

# Importa as classes base.
from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


# A classe 'UniformCostSearch' herda da classe abstrata 'SearchAlgorithm'.
class UniformCostSearch(SearchAlgorithm):
    """A3: Busca de Custo Uniforme (Dijkstra)"""

    # Implementação do método abstrato 'search'.
    def search(self, problem: Problem) -> Optional[Node]:
        # Cria o nó raiz.
        initial_node = Node(problem.initial_state)
        # Cria a fronteira como uma FILA DE PRIORIDADE. Cada item é uma tupla (custo, nó).
        # O 'heapq' usará o 'custo' para ordenar a fila.
        frontier = [(0, initial_node)]
        # Transforma a lista em uma fila de prioridade.
        heapq.heapify(frontier)
        # 'visited' agora é um dicionário para armazenar o menor custo encontrado para cada estado.
        visited = {}
        # Inicia os contadores.
        self.nodes_generated = 1
        self.nodes_visited = 0

        # Loop principal: continua enquanto houver nós na fronteira.
        while frontier:
            # Remove o nó com o MENOR CUSTO da fila de prioridade.
            cost, node = heapq.heappop(frontier)
            self.nodes_visited += 1

            # Otimização: se já encontramos um caminho mais barato para este estado, ignora.
            if node.state in visited and visited[node.state] < cost:
                continue

            # Verifica se o nó atual é o objetivo.
            if problem.is_goal(node.state):
                return node

            # Marca o estado como visitado, registrando seu custo.
            visited[node.state] = cost

            # Gera os filhos do nó atual.
            for child in self._get_successors(node, problem):
                # Se nunca vimos o filho OU se encontramos um caminho mais barato para ele...
                if child.state not in visited or child.path_cost < visited[child.state]:
                    # ...adiciona o filho à fronteira.
                    heapq.heappush(frontier, (child.path_cost, child))
        # Se a fronteira esvaziar, retorna falha.
        return None
