# -*- coding: utf-8 -*-

"""
Este arquivo define a classe Node, que representa um nó na árvore de busca.
Ele "envolve" um estado, adicionando informações de busca como pai, ação e custo.
"""

# 'from __future__ import annotations' permite usar anotações de tipo para classes
# que ainda não foram totalmente definidas, resolvendo importações circulares.
from __future__ import annotations
# Importa tipos para anotações de tipo.
from typing import List, Optional, TYPE_CHECKING

# Bloco especial para resolver importação circular com 'Problem' e 'State'.
# Este código só é executado por ferramentas de análise de tipo, não pelo Python em tempo de execução.
if TYPE_CHECKING:
    from problem.problem_interface import Problem
    from core.state import State

class Node:
    """
    Representa um nó na árvore de busca.
    Contém o estado, o nó pai, a ação que levou a este estado e o custo do caminho.
    """
    # O método construtor para criar um novo nó.
    def __init__(self, state: State, parent: Optional[Node] = None, action: Optional[str] = None, path_cost: float = 0):
        # O estado (configuração do tabuleiro) que este nó representa.
        self.state = state
        # Uma referência ao nó que gerou este nó (o "pai"). É None para o nó raiz.
        self.parent = parent
        # A ação que foi aplicada ao pai para gerar este nó (ex: 'CIMA').
        self.action = action
        # O custo acumulado desde o nó inicial até este nó (g(n) na A*).
        self.path_cost = path_cost
        # A profundidade do nó na árvore (quantos passos desde o início).
        self.depth = 0
        # Se houver um pai, a profundidade é a profundidade do pai + 1.
        if parent:
            self.depth = parent.depth + 1

    # Método mágico que define o comportamento do operador "menor que" (<).
    # É essencial para a Fila de Prioridade (heapq) saber como ordenar os nós.
    def __lt__(self, other):
        # A implementação padrão compara pelo custo do caminho.
        # Embora a A* e a Gulosa usem outros critérios na fronteira,
        # ter um comparador padrão é necessário para o heapq.
        return self.path_cost < other.path_cost

    # Método para gerar os nós filhos (sucessores) a partir do nó atual.
    def expand(self, problem: Problem) -> List[Node]:
        # Inicia uma lista vazia para os filhos.
        children = []
        # Pede ao objeto 'problem' para listar as ações válidas a partir do estado atual.
        for action in problem.get_actions(self.state):
            # Para cada ação, calcula o estado resultante.
            next_state = problem.get_result(self.state, action)
            # Calcula o custo do caminho para o filho.
            cost = self.path_cost + problem.get_cost(self.state, action)
            # Cria um novo nó filho e o adiciona à lista.
            children.append(Node(next_state, self, action, cost))
        # Retorna a lista de nós filhos gerados.
        return children

    # Método para reconstruir o caminho da solução.
    def get_path(self) -> List[State]:
        # Inicia uma lista vazia para o caminho.
        path = []
        # Começa a partir do nó atual.
        current = self
        # Loop que "sobe" na árvore, do nó atual até o nó raiz (que não tem pai).
        while current:
            # Adiciona o estado do nó atual ao caminho.
            path.append(current.state)
            # Move para o pai do nó atual.
            current = current.parent
        # A lista foi construída de trás para frente, então a invertemos para ter a ordem correta.
        return path[::-1]
