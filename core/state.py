# -*- coding: utf-8 -*-

"""
Este arquivo define a classe State, que representa uma configuração
do tabuleiro do 8-Puzzle. É a unidade de dados mais fundamental do projeto.
"""

# Importa o tipo 'Tuple' para usar em anotações de tipo (type hints).
from typing import Tuple


class State:
    """
    Representa um estado (configuração do tabuleiro) do 8-Puzzle.
    O estado é imutável para ser usado em conjuntos (sets) e dicionários de forma segura.
    O valor 0 representa o espaço vazio.
    """

    # O método construtor, chamado sempre que um novo objeto State é criado.
    def __init__(self, board: Tuple[int, ...]):
        # 'board: Tuple[int, ...]' é uma anotação de tipo que indica que 'board'
        # deve ser uma tupla de inteiros.

        # Verificação de segurança para garantir que o tabuleiro tenha o tamanho correto.
        if len(board) != 9:
            # Se não tiver, lança um erro claro para o desenvolvedor.
            raise ValueError("O tabuleiro deve ter 9 elementos.")

        # Armazena a tupla do tabuleiro como um atributo do objeto.
        self.board = board
        # Otimização: Pré-calcula e armazena a posição do espaço vazio (0)
        # para que não precisemos procurá-lo repetidamente.
        self.blank_pos = self.board.index(0)

    # Método mágico que define como o operador de igualdade (==) funciona.
    def __eq__(self, other):
        # Dois estados são iguais se 'other' também for um objeto State E
        # se seus tabuleiros forem idênticos.
        return isinstance(other, State) and self.board == other.board

    # Método mágico que retorna um valor de hash para o objeto.
    # É essencial para que objetos State possam ser adicionados a 'sets' e 'dicionários'.
    def __hash__(self):
        # Como a tupla 'self.board' é imutável, podemos usar seu hash diretamente.
        return hash(self.board)

    # Método mágico que define a representação em string do objeto (quando usamos print()).
    def __str__(self):
        # Converte cada número em string, junta tudo e substitui '0' por '_' para legibilidade.
        return "".join(map(str, self.board)).replace('0', '_')

    # Um método auxiliar para uma visualização mais amigável do tabuleiro.
    def to_matrix_str(self) -> str:
        # Cria uma lista de strings, substituindo o 0 por '_'.
        b = [str(x) if x != 0 else '_' for x in self.board]
        # Formata a lista em uma grade 3x3 com quebras de linha.
        return (f"{b[0]} {b[1]} {b[2]}\n"
                f"{b[3]} {b[4]} {b[5]}\n"
                f"{b[6]} {b[7]} {b[8]}")
