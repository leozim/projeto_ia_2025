# -*- coding: utf-8 -*-

"""
Contém funções auxiliares para o problema do 8-Puzzle.
Isso mantém o código principal mais limpo, separando responsabilidades.
"""

# Importa a biblioteca para funcionalidades aleatórias.
import random
# Importa tipos para anotações.
from typing import Tuple, List

# Importa as classes necessárias.
from core.state import State
from problem.eight_puzzle import EightPuzzleProblem


def is_solvable(board: Tuple[int, ...]) -> bool:
    """Verifica se uma configuração do 8-Puzzle é solucionável."""
    # O 8-Puzzle tem uma propriedade matemática: nem todas as configurações
    # iniciais podem ser resolvidas. Esta função verifica isso.
    inversions = 0
    # Cria uma lista sem o espaço vazio para contar as inversões.
    board_no_blank = [i for i in board if i != 0]
    # Loop para contar o número de "inversões".
    # Uma inversão é quando um número maior aparece antes de um número menor.
    for i in range(len(board_no_blank)):
        for j in range(i + 1, len(board_no_blank)):
            if board_no_blank[i] > board_no_blank[j]:
                inversions += 1
    # Para uma grade 3x3, o número de inversões deve ser par para que seja solucionável.
    return inversions % 2 == 0


def generate_random_state() -> State:
    """Gera um estado inicial aleatório e garantidamente solucionável."""
    # Loop infinito que só é quebrado quando um estado válido é encontrado.
    while True:
        # Cria uma lista de 0 a 8.
        board = list(range(9))
        # Embaralha a lista aleatoriamente.
        random.shuffle(board)
        # Converte para uma tupla.
        board_tuple = tuple(board)
        # Usa a função acima para verificar se a configuração é solucionável.
        if is_solvable(board_tuple):
            # Se for, cria o objeto State e o retorna, quebrando o loop.
            return State(board_tuple)


def calculate_path_cost(path: List[State], cost_type: str) -> float:
    """
    Calcula o custo de um caminho para uma dada função de custo.
    Útil para a Busca Gulosa, que não otimiza o custo do caminho durante a busca.
    """
    # Se o caminho for vazio ou tiver apenas um estado, o custo é 0.
    if not path or len(path) < 2:
        return 0.0

    # Inicia o contador de custo total.
    total_cost = 0
    # Cria um problema temporário apenas para ter acesso ao método 'get_cost'.
    temp_problem = EightPuzzleProblem(path[0], cost_type)

    # Loop que percorre o caminho de um estado para o próximo.
    for i in range(len(path) - 1):
        current_state = path[i]
        next_state = path[i + 1]

        # Determina qual ação levou do estado atual para o próximo,
        # analisando como a posição do espaço vazio mudou.
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
            continue  # Não deveria acontecer em um caminho válido.

        # Adiciona o custo daquela ação ao total.
        total_cost += temp_problem.get_cost(current_state, action)

    # Retorna o custo total calculado.
    return total_cost
