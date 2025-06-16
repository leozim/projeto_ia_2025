# -*- coding: utf-8 -*-

"""
Ponto de entrada principal para executar os experimentos do 8-Puzzle.

Para executar uma parte do experimento, descomente a chamada de função
`runner.run_experiment` correspondente.
"""

from runner import ExperimentRunner
from algorithms import (
    BreadthFirstSearch,
    DepthFirstSearch,
    UniformCostSearch,
    GreedyBestFirstSearch,
    AStarSearch
)


def main():
    """Define e executa os cenários de teste para o trabalho."""
    runner = ExperimentRunner(output_dir="results")
    all_cost_types = ['C1', 'C2', 'C3', 'C4']
    all_heuristics = ['H1', 'H2']

    # --- Parte 1: Largura vs. Profundidade vs. Custo Uniforme ---
    print("Definindo cenários da Parte 1...")
    part1_scenarios = []
    for algo in [BreadthFirstSearch, DepthFirstSearch, UniformCostSearch]:
        for cost in all_cost_types:
            part1_scenarios.append({'algorithm': algo, 'cost_type': cost})
    runner.run_experiment("Part1", part1_scenarios, num_runs=30)

    # --- Parte 2: Custo Uniforme vs. A* ---
    print("Definindo cenários da Parte 2...")
    part2_scenarios = []
    for cost in all_cost_types:
        part2_scenarios.append({'algorithm': UniformCostSearch, 'cost_type': cost})
        for heuristic in all_heuristics:
            part2_scenarios.append({'algorithm': AStarSearch, 'cost_type': cost, 'heuristic': heuristic})
    runner.run_experiment("Part2", part2_scenarios, num_runs=30)

    # --- Parte 3: Busca Gulosa vs. A* ---
    print("Definindo cenários da Parte 3...")
    part3_scenarios = []
    for heuristic in all_heuristics:
        # CORREÇÃO: Usamos 'C1' como um custo padrão para evitar o erro.
        # A Busca Gulosa não usa o custo do caminho durante a busca, e o runner.py
        # recalcula o custo correto para todas as funções de custo (C1-C4) no final.
        part3_scenarios.append({
            'algorithm': GreedyBestFirstSearch,
            'heuristic': heuristic,
            'cost_type': 'C1'}) # Alterado de 'N/A' para 'C1'
    for cost in all_cost_types:
        for heuristic in all_heuristics:
            part3_scenarios.append({'algorithm': AStarSearch, 'cost_type': cost, 'heuristic': heuristic})
    runner.run_experiment("Part3", part3_scenarios, num_runs=30)

    # --- Parte 4: Randomização da Vizinhança ---
    print("Definindo cenários da Parte 4...")
    part4_scenarios = []
    for algo in [BreadthFirstSearch, DepthFirstSearch]:
        for cost in all_cost_types:
            part4_scenarios.append({
                'algorithm': algo,
                'cost_type': cost,
                'random_successors': True,
                'executions': 10
            })
    runner.run_experiment("Part4", part4_scenarios, num_runs=15)

    print("\nTodos os experimentos selecionados foram concluídos.")
    print("Verifique a pasta 'results' para os arquivos CSV gerados.")


if __name__ == '__main__':
    main()
