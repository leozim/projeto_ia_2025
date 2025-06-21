# -*- coding: utf-8 -*-

"""
Este arquivo define a classe Node, que representa um nó na árvore de busca.
"""

from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

# Evita importação circular, permitindo anotações de tipo
if TYPE_CHECKING:
    from problem.problem_interface import Problem
    from core.state import State

class Node:
    """
    Representa um nó na árvore de busca.
    Contém o estado, o nó pai, a ação que levou a este estado e o custo do caminho.
    """
    def __init__(self, state: State, parent: Optional[Node] = None, action: Optional[str] = None, path_cost: float = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    #magic method less than
    def __lt__(self, other):
        # Comparador necessário para a fila de prioridade (heapq).
        return self.path_cost < other.path_cost

    def expand(self, problem: Problem) -> List[Node]:
        """Gera os nós filhos (sucessores) a partir do nó atual."""
        children = []
        for action in problem.get_actions(self.state):
            next_state = problem.get_result(self.state, action)
            cost = self.path_cost + problem.get_cost(self.state, action)
            children.append(Node(next_state, self, action, cost))
        return children

    def get_path(self) -> List[State]:
        """Retorna a sequência de estados do início até o nó atual."""
        path = []
        current = self
        while current:
            path.append(current.state)
            current = current.parent
        return path[::-1]  # Inverte para ter a ordem correta (início -> fim)
