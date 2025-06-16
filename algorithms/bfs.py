# -*- coding: utf-8 -*-
from collections import deque
from typing import Optional

from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


class BreadthFirstSearch(SearchAlgorithm):
    """A1: Busca em Largura (BFS)"""

    def search(self, problem: Problem) -> Optional[Node]:
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
                if child.state not in visited:
                    if problem.is_goal(child.state):
                        return child
                    frontier.append(child)
                    visited.add(child.state)
        return None
