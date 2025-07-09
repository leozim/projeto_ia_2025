# -*- coding: utf-8 -*-

"""
Implementação concreta do problema do 8-Puzzle, com suas variações
de custo e heurísticas. Esta classe "cumpre o contrato" definido em Problem.
"""

# Importa tipos para anotações.
from typing import List, Tuple, Dict, Optional

# Importa as classes base.
from core.state import State
from problem.problem_interface import Problem


# A classe 'EightPuzzleProblem' herda da classe abstrata 'Problem'.
class EightPuzzleProblem(Problem):
    """
    Implementação do problema 8-Puzzle com suas variações de custo e heurísticas.
    """
    # Atributos de classe (compartilhados por todas as instâncias) para otimização.
    # Eles armazenam dados pré-calculados para evitar trabalho repetido.
    _goal_states: List[State] = []  # Lista dos 9 estados de solução.
    _goal_coords: Dict[State, Dict[int, Tuple[int, int]]] = {}  # Mapa de coordenadas das peças para cada solução.

    # O construtor da classe.
    def __init__(self, initial_state: State, cost_type: str, heuristic_type: Optional[str] = None):
        # Chama o construtor da classe pai ('Problem') para inicializar os atributos comuns.
        super().__init__(initial_state, cost_type, heuristic_type)
        # Otimização: Se a lista de estados objetivo ainda não foi preenchida...
        if not EightPuzzleProblem._goal_states:
            # ...chama o método para gerá-los. Isso só acontece uma vez.
            self._generate_goals()

    # Método "privado" para gerar os dados dos estados objetivo.
    def _generate_goals(self):
        # Cria a sequência base de peças ordenadas (1 a 8).
        base_goal = tuple(range(1, 9))
        # Loop para criar os 9 estados de solução (um para cada posição do espaço vazio).
        for i in range(9):
            # Cria uma cópia modificável da base.
            goal_list = list(base_goal)
            # Insere o espaço vazio (0) na posição 'i'.
            goal_list.insert(i, 0)
            # Cria o objeto State para esta solução.
            goal_state = State(tuple(goal_list))
            # Adiciona o estado de solução à lista de classe.
            EightPuzzleProblem._goal_states.append(goal_state)

            # Inicia um dicionário para as coordenadas das peças desta solução.
            coords = {}
            # Loop para mapear cada peça à sua coordenada (linha, coluna).
            for idx, piece in enumerate(goal_state.board):
                if piece != 0:  # Ignora o espaço vazio.
                    coords[piece] = (idx // 3, idx % 3)
            # Armazena o mapa de coordenadas no dicionário de classe principal.
            EightPuzzleProblem._goal_coords[goal_state] = coords

    # Implementação do método abstrato 'get_actions'.
    def get_actions(self, state: State) -> List[str]:
        # Inicia uma lista vazia para as ações válidas.
        actions = []
        # Converte a posição linear do espaço vazio em coordenadas (linha, coluna).
        row, col = state.blank_pos // 3, state.blank_pos % 3
        # Verifica as bordas para determinar os movimentos possíveis.
        if row > 0: actions.append('CIMA')
        if row < 2: actions.append('BAIXO')
        if col > 0: actions.append('ESQUERDA')
        if col < 2: actions.append('DIREITA')
        # Retorna a lista de ações permitidas.
        return actions

    # Implementação do método abstrato 'get_result'.
    def get_result(self, state: State, action: str) -> State:
        # Cria uma cópia modificável do tabuleiro.
        board_list = list(state.board)
        blank_pos = state.blank_pos
        swap_pos = -1  # Posição da peça a ser trocada com o espaço vazio.

        # Calcula a posição de troca com base na ação.
        if action == 'CIMA':
            swap_pos = blank_pos - 3
        elif action == 'BAIXO':
            swap_pos = blank_pos + 3
        elif action == 'ESQUERDA':
            swap_pos = blank_pos - 1
        elif action == 'DIREITA':
            swap_pos = blank_pos + 1

        # Realiza a troca de posições na lista.
        board_list[blank_pos], board_list[swap_pos] = board_list[swap_pos], board_list[blank_pos]
        # Retorna um novo objeto State com o tabuleiro modificado.
        return State(tuple(board_list))

    # Implementação do método abstrato 'is_goal'.
    def is_goal(self, state: State) -> bool:
        # Verifica de forma eficiente se o estado atual está na lista pré-calculada de soluções.
        return state in self._goal_states

    # Implementação do método abstrato 'get_cost'.
    def get_cost(self, state: State, action: str) -> float:
        # Roteador que retorna o custo com base no 'cost_type' definido.
        if self.cost_type == 'C1':
            return 2.0

        is_vertical = action in ['CIMA', 'BAIXO']

        if self.cost_type == 'C2':
            return 2.0 if is_vertical else 3.0

        if self.cost_type == 'C3':
            return 3.0 if is_vertical else 2.0

        if self.cost_type == 'C4':
            next_state = self.get_result(state, action)
            if next_state.blank_pos == 4:  # Se o movimento leva o espaço para o centro.
                return 5.0
            return 2.0 if is_vertical else 3.0

        # Lança um erro se o tipo de custo for desconhecido.
        raise ValueError(f"Tipo de custo desconhecido: {self.cost_type}")

    # Implementação do método abstrato 'get_heuristic'.
    def get_heuristic(self, state: State) -> float:
        # Se nenhuma heurística for solicitada, retorna 0.
        if not self.heuristic_type:
            return 0.0

        # Lógica para a Heurística H1 (Peças Fora do Lugar).
        if self.heuristic_type == 'H1':
            min_misplaced = float('inf')
            # Para garantir admissibilidade, calcula a heurística em relação a cada objetivo
            # e pega o menor valor.
            for goal_state in self._goal_states:
                misplaced_count = sum(
                    1 for i in range(9) if state.board[i] != 0 and state.board[i] != goal_state.board[i])
                min_misplaced = min(min_misplaced, misplaced_count)
            return min_misplaced * 2.0

        # Lógica para a Heurística H2 (Distância de Manhattan).
        if self.heuristic_type == 'H2':
            min_manhattan_sum = float('inf')
            current_coords = {piece: (i // 3, i % 3) for i, piece in enumerate(state.board) if piece != 0}

            # Também calcula em relação a cada objetivo para garantir admissibilidade.
            for goal_state in self._goal_states:
                goal_piece_coords = self._goal_coords[goal_state]
                total_dist = 0
                for piece, (r1, c1) in current_coords.items():
                    r2, c2 = goal_piece_coords[piece]
                    total_dist += abs(r1 - r2) + abs(c1 - c2)
                min_manhattan_sum = min(min_manhattan_sum, total_dist)
            return min_manhattan_sum * 2.0

        # Lança um erro se o tipo de heurística for desconhecido.
        raise ValueError(f"Tipo de heurística desconhecido: {self.heuristic_type}")
