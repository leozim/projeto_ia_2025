# -*- coding: utf-8 -*-
from typing import Optional

from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


class DepthFirstSearch(SearchAlgorithm):
    """
    A2: Busca em Profundidade (DFS)

    CORREÇÃO: Implementado com um limite de profundidade para garantir que o algoritmo
    sempre termine e não se perca em ramos infinitos da árvore de busca.
    """

    def __init__(self, randomize_successors: bool = False, depth_limit: int = 30):
        super().__init__(randomize_successors)
        self.depth_limit = depth_limit  # Adiciona um limite de profundidade

    def search(self, problem: Problem) -> Optional[Node]:
        initial_node = Node(problem.initial_state)

        frontier = [initial_node]  # Pilha (LIFO)
        visited = set()
        self.nodes_generated = 1
        self.nodes_visited = 0

        while frontier:
            node = frontier.pop()

            if problem.is_goal(node.state):
                return node

            # Verifica se o limite de profundidade foi atingido
            if node.depth >= self.depth_limit:
                continue

            self.nodes_visited += 1
            visited.add(node.state)

            # Adiciona filhos à fronteira se não foram visitados
            for child in reversed(self._get_successors(node, problem)):
                if child.state not in visited:
                    frontier.append(child)

        # Se a fronteira ficar vazia e nenhuma solução foi encontrada, retorna falha
        return None
