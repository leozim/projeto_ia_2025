# -*- coding: utf-8 -*-

"""
Este arquivo define a classe State, que representa uma configuração
do tabuleiro do 8-Puzzle.
"""

from typing import Tuple

class State:
    """
    Representa um estado (configuração do tabuleiro) do 8-Puzzle.
    O estado é imutável para ser usado em conjuntos (sets) e dicionários de forma segura.
    O valor 0 representa o espaço vazio.
    """
    def __init__(self, board: Tuple[int, ...]):
        if len(board) != 9:
            raise ValueError("O tabuleiro deve ter 9 elementos.")
        self.board = board
        # Pré-calcula e armazena a posição do espaço vazio para acesso rápido.
        self.blank_pos = self.board.index(0)

    def __eq__(self, other):
        return isinstance(other, State) and self.board == other.board

    def __hash__(self):
        return hash(self.board)

    def __str__(self):
        return "".join(map(str, self.board)).replace('0', '_')

    def to_matrix_str(self) -> str:
        """Retorna uma representação do estado em formato de matriz 3x3."""
        b = [str(x) if x != 0 else '_' for x in self.board]
        return (f"{b[0]} {b[1]} {b[2]}\n"
                f"{b[3]} {b[4]} {b[5]}\n"
                f"{b[6]} {b[7]} {b[8]}")
