# -*- coding: utf-8 -*-
import heapq
from typing import Optional

from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


class AStarSearch(SearchAlgorithm):
    """A5: Busca A*"""

    def search(self, problem: Problem) -> Optional[Node]:
        initial_node = Node(problem.initial_state)
        h_val = problem.get_heuristic(initial_node.state)
        # f(n) = g(n) + h(n), onde g(n) é node.path_cost
        frontier = [(initial_node.path_cost + h_val, initial_node)]  # Fila de Prioridade por f(n)
        heapq.heapify(frontier)
        visited = {initial_node.state: 0}  # Armazena g(n) para cada estado
        self.nodes_generated = 1
        self.nodes_visited = 0

        while frontier:
            f_cost, node = heapq.heappop(frontier)
            self.nodes_visited += 1

            if node.path_cost > visited[node.state]:
                continue

            if problem.is_goal(node.state):
                return node

            for child in self._get_successors(node, problem):
                g_child = child.path_cost
                if child.state not in visited or g_child < visited[child.state]:
                    visited[child.state] = g_child
                    h_child = problem.get_heuristic(child.state)
                    f_child = g_child + h_child
                    heapq.heappush(frontier, (f_child, child))
        return None
