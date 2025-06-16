# -*- coding: utf-8 -*-

"""
Define a interface (classe abstrata) para um problema de busca.
"""

from abc import ABC, abstractmethod
from typing import List

from core.state import State

class Problem(ABC):
    """
    Classe abstrata para formalizar um problema de busca.
    Isso permite que os algoritmos de busca sejam genéricos e não acoplados ao 8-Puzzle.
    """
    def __init__(self, initial_state: State, cost_type: str, heuristic_type: str | None = None):
        self.initial_state = initial_state
        self.cost_type = cost_type
        self.heuristic_type = heuristic_type

    @abstractmethod
    def get_actions(self, state: State) -> List[str]:
        """Retorna as ações possíveis a partir de um estado."""
        pass

    @abstractmethod
    def get_result(self, state: State, action: str) -> State:
        """Retorna o estado resultante da aplicação de uma ação."""
        pass

    @abstractmethod
    def is_goal(self, state: State) -> bool:
        """Verifica se um estado é o objetivo."""
        pass

    @abstractmethod
    def get_cost(self, state: State, action: str) -> float:
        """Calcula o custo de uma ação em um determinado estado."""
        pass

    @abstractmethod
    def get_heuristic(self, state: State) -> float:
        """Calcula o valor da heurística para um estado."""
        pass
