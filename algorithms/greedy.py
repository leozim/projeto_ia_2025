# -*- coding: utf-8 -*-
import heapq
from typing import Optional

from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


class GreedyBestFirstSearch(SearchAlgorithm):
    """A4: Busca Gulosa"""

    def search(self, problem: Problem) -> Optional[Node]:
        initial_node = Node(problem.initial_state)
        h_val = problem.get_heuristic(initial_node.state)
        frontier = [(h_val, initial_node)]  # Fila de Prioridade por h(n)
        heapq.heapify(frontier)
        visited = {initial_node.state}
        self.nodes_generated = 1
        self.nodes_visited = 0

        while frontier:
            _, node = heapq.heappop(frontier)
            self.nodes_visited += 1

            if problem.is_goal(node.state):
                return node

            for child in self._get_successors(node, problem):
                if child.state not in visited:
                    visited.add(child.state)
                    h_child = problem.get_heuristic(child.state)
                    heapq.heappush(frontier, (h_child, child))
        return None
