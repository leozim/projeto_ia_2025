# -*- coding: utf-8 -*-

# Importa tipos para anotações.
from typing import Optional

# Importa as classes base.
from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


# A classe 'DepthFirstSearch' herda da classe abstrata 'SearchAlgorithm'.
class DepthFirstSearch(SearchAlgorithm):
    """
    A2: Busca em Profundidade (DFS)
    Implementado com um limite de profundidade para garantir que o algoritmo
    sempre termine e não se perca em ramos infinitos da árvore de busca.
    """

    # O construtor é estendido para aceitar um limite de profundidade.
    def __init__(self, randomize_successors: bool = False, depth_limit: int = 30):
        # Chama o construtor da classe pai.
        super().__init__(randomize_successors)
        # Armazena o limite de profundidade.
        self.depth_limit = depth_limit

    # Implementação do método abstrato 'search'.
    def search(self, problem: Problem) -> Optional[Node]:
        # Cria o nó raiz.
        initial_node = Node(problem.initial_state)

        # Cria a fronteira como uma PILHA (LIFO), usando uma lista normal.
        frontier = [initial_node]
        # Cria o conjunto de visitados.
        visited = set()
        # Inicia os contadores.
        self.nodes_generated = 1
        self.nodes_visited = 0

        # Loop principal: continua enquanto houver nós na fronteira.
        while frontier:
            # Remove o nó do TOPO da pilha (o mais recente).
            node = frontier.pop()

            # Verifica se o nó atual é o objetivo.
            if problem.is_goal(node.state):
                return node

            # Medida de segurança: se o nó atingiu o limite de profundidade, ignora-o.
            if node.depth >= self.depth_limit:
                continue

            # Adiciona o estado aos visitados para não processá-lo novamente.
            self.nodes_visited += 1
            visited.add(node.state)

            # Gera os filhos do nó atual. 'reversed' é usado para que a primeira ação
            # seja a primeira a ser explorada.
            for child in reversed(self._get_successors(node, problem)):
                # Se o estado do filho nunca foi visto antes...
                if child.state not in visited:
                    # ...adiciona ao topo da pilha da fronteira.
                    frontier.append(child)

        # Se a fronteira esvaziar, retorna falha.
        return None
