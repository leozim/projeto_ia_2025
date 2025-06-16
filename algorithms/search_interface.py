# -*- coding: utf-8 -*-

"""
Define a interface (classe abstrata) para um algoritmo de busca.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
import random

from core.node import Node
from problem.problem_interface import Problem


class SearchAlgorithm(ABC):
    """Classe base para os algoritmos de busca, com lógica compartilhada."""

    def __init__(self, randomize_successors: bool = False):
        self.randomize = randomize_successors
        self.nodes_generated = 0
        self.nodes_visited = 0

    @abstractmethod
    def search(self, problem: Problem) -> Optional[Node]:
        """Executa a busca e retorna o nó objetivo ou None se falhar."""
        pass

    def _get_successors(self, node: Node, problem: Problem) -> List[Node]:
        """Gera sucessores, com opção de embaralhar a ordem para o Experimento 4."""
        successors = node.expand(problem)
        self.nodes_generated += len(successors)
        if self.randomize:
            random.shuffle(successors)
        return successors
