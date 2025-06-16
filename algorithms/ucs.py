# -*- coding: utf-8 -*-
import heapq
from typing import Optional

from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


class UniformCostSearch(SearchAlgorithm):
    """A3: Busca de Custo Uniforme (Dijkstra)"""

    def search(self, problem: Problem) -> Optional[Node]:
        initial_node = Node(problem.initial_state)
        frontier = [(0, initial_node)]  # (cost, node) - Fila de Prioridade
        heapq.heapify(frontier)
        visited = {}  # Dicionário para armazenar o menor custo para cada estado
        self.nodes_generated = 1
        self.nodes_visited = 0

        while frontier:
            cost, node = heapq.heappop(frontier)
            self.nodes_visited += 1

            if node.state in visited and visited[node.state] < cost:
                continue

            if problem.is_goal(node.state):
                return node

            visited[node.state] = cost

            for child in self._get_successors(node, problem):
                if child.state not in visited or child.path_cost < visited[child.state]:
                    heapq.heappush(frontier, (child.path_cost, child))
        return None
