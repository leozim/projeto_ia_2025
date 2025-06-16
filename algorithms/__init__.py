# -*- coding: utf-8 -*-

"""
Torna o diretório 'algorithms' um pacote Python e exporta as classes
de algoritmo para facilitar a importação.
"""

from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch
from .ucs import UniformCostSearch
from .greedy import GreedyBestFirstSearch
from .astar import AStarSearch

__all__ = [
    'BreadthFirstSearch',
    'DepthFirstSearch',
    'UniformCostSearch',
    'GreedyBestFirstSearch',
    'AStarSearch'
]
