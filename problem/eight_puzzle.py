# -*- coding: utf-8 -*-

"""
Implementação concreta do problema do 8-Puzzle, com suas variações
de custo e heurísticas.
"""

from typing import List, Tuple, Dict

from core.state import State
from problem.problem_interface import Problem


class EightPuzzleProblem(Problem):
    """
    Implementação do problema 8-Puzzle com suas variações de custo e heurísticas.
    """
    _goal_states: List[State] = []
    _goal_coords: Dict[State, Dict[int, Tuple[int, int]]] = {}

    def __init__(self, initial_state: State, cost_type: str, heuristic_type: str | None = None):
        super().__init__(initial_state, cost_type, heuristic_type)
        if not EightPuzzleProblem._goal_states:
            self._generate_goals()

    def _generate_goals(self):
        """Gera e armazena os 9 estados objetivo e as coordenadas das peças."""
        base_goal = tuple(range(1, 9))
        for i in range(9):
            goal_list = list(base_goal)
            goal_list.insert(i, 0)
            goal_state = State(tuple(goal_list))
            EightPuzzleProblem._goal_states.append(goal_state)

            coords = {}
            for idx, piece in enumerate(goal_state.board):
                if piece != 0:
                    coords[piece] = (idx // 3, idx % 3)
            EightPuzzleProblem._goal_coords[goal_state] = coords

    def get_actions(self, state: State) -> List[str]:
        """Retorna as ações possíveis (CIMA, BAIXO, ESQUERDA, DIREITA)."""
        actions = []
        row, col = state.blank_pos // 3, state.blank_pos % 3
        if row > 0: actions.append('CIMA')
        if row < 2: actions.append('BAIXO')
        if col > 0: actions.append('ESQUERDA')
        if col < 2: actions.append('DIREITA')
        return actions

    def get_result(self, state: State, action: str) -> State:
        """Move o espaço vazio e retorna um novo objeto State."""
        board_list = list(state.board)
        blank_pos = state.blank_pos
        swap_pos = -1

        if action == 'CIMA':
            swap_pos = blank_pos - 3
        elif action == 'BAIXO':
            swap_pos = blank_pos + 3
        elif action == 'ESQUERDA':
            swap_pos = blank_pos - 1
        elif action == 'DIREITA':
            swap_pos = blank_pos + 1

        board_list[blank_pos], board_list[swap_pos] = board_list[swap_pos], board_list[blank_pos]
        return State(tuple(board_list))

    def is_goal(self, state: State) -> bool:
        """Verifica se o estado corresponde a um dos 9 objetivos."""
        return state in self._goal_states

    def get_cost(self, state: State, action: str) -> float:
        """Implementa as funções de custo C1, C2, C3, C4."""
        if self.cost_type == 'C1':
            return 2.0

        is_vertical = action in ['CIMA', 'BAIXO']

        if self.cost_type == 'C2':
            return 2.0 if is_vertical else 3.0

        if self.cost_type == 'C3':
            return 3.0 if is_vertical else 2.0

        if self.cost_type == 'C4':
            next_state = self.get_result(state, action)
            if next_state.blank_pos == 4:
                return 5.0
            return 2.0 if is_vertical else 3.0

        raise ValueError(f"Tipo de custo desconhecido: {self.cost_type}")

    def get_heuristic(self, state: State) -> float:
        """Implementa as heurísticas H1 e H2, garantindo admissibilidade."""
        if not self.heuristic_type:
            return 0.0

        if self.heuristic_type == 'H1':
            min_misplaced = float('inf')
            for goal_state in self._goal_states:
                misplaced_count = sum(
                    1 for i in range(9) if state.board[i] != 0 and state.board[i] != goal_state.board[i])
                min_misplaced = min(min_misplaced, misplaced_count)
            return min_misplaced * 2.0

        if self.heuristic_type == 'H2':
            min_manhattan_sum = float('inf')
            current_coords = {piece: (i // 3, i % 3) for i, piece in enumerate(state.board) if piece != 0}

            for goal_state in self._goal_states:
                goal_piece_coords = self._goal_coords[goal_state]
                total_dist = 0
                for piece, (r1, c1) in current_coords.items():
                    r2, c2 = goal_piece_coords[piece]
                    total_dist += abs(r1 - r2) + abs(c1 - c2)
                min_manhattan_sum = min(min_manhattan_sum, total_dist)
            return min_manhattan_sum * 2.0

        raise ValueError(f"Tipo de heurística desconhecido: {self.heuristic_type}")

