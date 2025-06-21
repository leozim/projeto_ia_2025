# -*- coding: utf-8 -*-
from collections import deque
from typing import Optional

from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


class BreadthFirstSearch(SearchAlgorithm):
    """A1: Busca em Largura (BFS)"""

    def search(self, problem: Problem) -> Optional[Node]:
        # Cria o primeiro nó (a raiz da árvore de busca) com o estado inicial do problema.
        initial_node = Node(problem.initial_state)
        if problem.is_goal(initial_node.state):
            return initial_node

        frontier = deque([initial_node])  # Fila (FIFO)
        visited = {initial_node.state}
        self.nodes_generated = 1
        self.nodes_visited = 0

        while frontier:
            node = frontier.popleft()
            self.nodes_visited += 1

            for child in self._get_successors(node, problem):
                # VERIFICA SE JÁ VIMOS ESTE ESTADO: A condição mais importante.
                # Se o estado do nó filho ainda não estiver no nosso conjunto de 'visitados'
                # Evita estado-loop
                if child.state not in visited:
                    if problem.is_goal(child.state):
                        return child
                    frontier.append(child)
                    visited.add(child.state)
        # Se o loop 'while' terminar (ou seja, a fronteira ficou vazia),
        # significa que exploramos todos os estados alcançáveis e não encontramos
        # uma solução. A função retorna 'None' para indicar falha.
        return None
