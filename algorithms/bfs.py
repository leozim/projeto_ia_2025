# -*- coding: utf-8 -*-

# Importa a estrutura de dados 'deque', uma fila eficiente.
from collections import deque
# Importa tipos para anotações.
from typing import Optional

# Importa as classes base.
from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


# A classe 'BreadthFirstSearch' herda da classe abstrata 'SearchAlgorithm'.
class BreadthFirstSearch(SearchAlgorithm):
    """A1: Busca em Largura (BFS)"""

    # Implementação do método abstrato 'search'.
    def search(self, problem: Problem) -> Optional[Node]:
        # Cria o nó raiz.
        initial_node = Node(problem.initial_state)
        # Verifica se o estado inicial já é a solução.
        if problem.is_goal(initial_node.state):
            return initial_node

        # Cria a fronteira como uma FILA (FIFO), começando com o nó inicial.
        frontier = deque([initial_node])
        # Cria o conjunto de visitados para evitar loops.
        visited = {initial_node.state}
        # Inicia os contadores.
        self.nodes_generated = 1
        self.nodes_visited = 0

        # Loop principal: continua enquanto houver nós na fronteira.
        while frontier:
            # Remove o nó da FRENTE da fila (o mais antigo).
            node = frontier.popleft()
            self.nodes_visited += 1

            # Gera os filhos do nó atual.
            for child in self._get_successors(node, problem):
                # Se o estado do filho nunca foi visto antes...
                if child.state not in visited:
                    # ...verifica se é o objetivo.
                    if problem.is_goal(child.state):
                        return child  # Se for, retorna a solução.
                    # Se não for o objetivo, adiciona à fronteira e aos visitados.
                    frontier.append(child)
                    visited.add(child.state)
        # Se a fronteira esvaziar, retorna falha.
        return None
