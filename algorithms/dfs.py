# -*- coding: utf-8 -*-
from typing import Optional

from core.node import Node
from problem.problem_interface import Problem
from .search_interface import SearchAlgorithm


class DepthFirstSearch(SearchAlgorithm):
    """
    A2: Busca em Profundidade (DFS)

    CORREÇÃO: Implementado com um limite de profundidade para garantir que o algoritmo
    sempre termine e não se perca em ramos infinitos da árvore de busca.
    """

    def __init__(self, randomize_successors: bool = False, depth_limit: int = 30):
        super().__init__(randomize_successors)
        self.depth_limit = depth_limit  # Adiciona um limite de profundidade

    def search(self, problem: Problem) -> Optional[Node]:
        initial_node = Node(problem.initial_state)

        # CRIA A FRONTEIRA: Aqui está a 1ª diferença crucial. Usamos uma lista
        # do Python, que funcionará como uma Pilha (Stack).
        # A fronteira começa contendo apenas o nó inicial.
        frontier = [initial_node]  # Pilha (LIFO)

        # CRIA O CONJUNTO DE VISITADOS: O propósito é o mesmo da BFS - evitar loops.
        # No entanto, a lógica de quando adicionamos a ele é um pouco diferente.
        visited = set()
        self.nodes_generated = 1
        self.nodes_visited = 0

        while frontier:
            node = frontier.pop() # remove o ultimo elemento da lista[ultimo adicionado]

            if problem.is_goal(node.state):
                return node

            # Verifica se o limite de profundidade foi atingido
            if node.depth >= self.depth_limit:
                continue

            # MARCA COMO VISITADO: Adicionamos o estado ao conjunto de 'visitados'
            # APÓS retirá-lo da pilha, para garantir que não o processemos novamente.
            self.nodes_visited += 1
            visited.add(node.state)

            # Adiciona filhos à fronteira se não foram visitados
            # Geramos todos os filhos do nó atual.
            # Usamos 'reversed()' para que os nós sejam adicionados à pilha de forma que
            # a primeira ação (ex: 'CIMA') seja explorada primeiro, o que é mais intuitivo.
            for child in reversed(self._get_successors(node, problem)):
                if child.state not in visited:
                    frontier.append(child)

        # Se a fronteira ficar vazia e nenhuma solução foi encontrada, retorna falha
        return None
