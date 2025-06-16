# -*- coding: utf-8 -*-

"""
Contém funções auxiliares para o problema do 8-Puzzle, como
verificar se é solucionável e gerar estados aleatórios.
"""

import random
from typing import Tuple, List

from core.state import State
from problem.eight_puzzle import EightPuzzleProblem


def is_solvable(board: Tuple[int, ...]) -> bool:
    """Verifica se uma configuração do 8-Puzzle é solucionável."""
    inversions = 0
    board_no_blank = [i for i in board if i != 0]
    for i in range(len(board_no_blank)):
        for j in range(i + 1, len(board_no_blank)):
            if board_no_blank[i] > board_no_blank[j]:
                inversions += 1
    # Para uma grade 3x3, o número de inversões deve ser par.
    return inversions % 2 == 0


def generate_random_state() -> State:
    """Gera um estado inicial aleatório e garantidamente solucionável."""
    while True:
        board = list(range(9))
        random.shuffle(board)
        board_tuple = tuple(board)
        if is_solvable(board_tuple):
            return State(board_tuple)


def calculate_path_cost(path: List[State], cost_type: str) -> float:
    """
    Calcula o custo de um caminho para uma dada função de custo.
    Útil para a Busca Gulosa, que não otimiza o custo do caminho.
    """
    if not path or len(path) < 2:
        return 0.0

    total_cost = 0
    temp_problem = EightPuzzleProblem(path[0], cost_type)

    for i in range(len(path) - 1):
        current_state = path[i]
        next_state = path[i + 1]

        blank_diff = next_state.blank_pos - current_state.blank_pos
        action = ''
        if blank_diff == -3:
            action = 'CIMA'
        elif blank_diff == 3:
            action = 'BAIXO'
        elif blank_diff == -1:
            action = 'ESQUERDA'
        elif blank_diff == 1:
            action = 'DIREITA'
        else:
            continue

        total_cost += temp_problem.get_cost(current_state, action)

    return total_cost
