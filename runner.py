# -*- coding: utf-8 -*-

"""
Define a classe ExperimentRunner, responsável por orquestrar a execução
dos experimentos, coletar dados e salvá-los em arquivos CSV.
"""

import os
import csv
import time
from typing import List, Dict

from problem.eight_puzzle import EightPuzzleProblem
from algorithms import GreedyBestFirstSearch
from utils.puzzle_utils import generate_random_state, calculate_path_cost


class ExperimentRunner:
    """Orquestra a execução dos experimentos e salva os resultados em CSV."""

    def __init__(self, output_dir="results"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def run_experiment(self, part_name: str, scenarios: List[Dict], num_runs: int):
        """
        Executa uma parte do experimento.
        :param part_name: Nome da parte (e.g., "Part1")
        :param scenarios: Lista de dicionários, cada um definindo um cenário de teste.
        :param num_runs: Número de estados iniciais aleatórios a serem testados.
        """
        filepath = os.path.join(self.output_dir, f"{part_name}_results.csv")
        headers = [
            'run_id', 'initial_state', 'algorithm', 'cost_function', 'heuristic', 'random_successors',
            'goal_state_found', 'path_length', 'path_cost', 'nodes_generated', 'nodes_visited', 'execution_time_sec'
        ]

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            print(f"\n--- Iniciando Experimento: {part_name} ---")
            run_id_counter = 1

            for i in range(num_runs):
                initial_state = generate_random_state()
                print(f"  Run {i + 1}/{num_runs} com Estado Inicial: {initial_state}")

                for scenario in scenarios:
                    algo_class = scenario['algorithm']
                    cost_type = scenario.get('cost_type')
                    heuristic_type = scenario.get('heuristic')
                    random_succ = scenario.get('random_successors', False)
                    num_executions = scenario.get('executions', 1)

                    for exec_count in range(num_executions):
                        print(
                            f"    Executando: {algo_class.__name__}, Custo={cost_type or 'N/A'}, Heuristica={heuristic_type or 'N/A'}, Rand={random_succ} ({exec_count + 1}/{num_executions})")

                        problem = EightPuzzleProblem(initial_state, cost_type, heuristic_type)
                        algorithm = algo_class(randomize_successors=random_succ)

                        start_time = time.time()
                        solution_node = algorithm.search(problem)
                        end_time = time.time()

                        result_base = {
                            'run_id': run_id_counter,
                            'initial_state': str(initial_state),
                            'algorithm': algo_class.__name__,
                            'heuristic': heuristic_type or 'N/A',
                            'random_successors': random_succ,
                            'execution_time_sec': round(end_time - start_time, 4),
                            'nodes_generated': algorithm.nodes_generated,
                            'nodes_visited': algorithm.nodes_visited,
                        }

                        if solution_node:
                            path_states = solution_node.get_path()

                            if algo_class is GreedyBestFirstSearch:
                                for c_type in ['C1', 'C2', 'C3', 'C4']:
                                    recalculated_cost = calculate_path_cost(path_states, c_type)
                                    writer.writerow({**result_base,
                                                     'cost_function': c_type,
                                                     'goal_state_found': str(solution_node.state),
                                                     'path_length': solution_node.depth,
                                                     'path_cost': recalculated_cost,
                                                     })
                                run_id_counter += 1
                                continue

                            result_base.update({
                                'cost_function': cost_type,
                                'goal_state_found': str(solution_node.state),
                                'path_length': solution_node.depth,
                                'path_cost': solution_node.path_cost,
                            })
                        else:
                            result_base.update({
                                'cost_function': cost_type,
                                'goal_state_found': 'None',
                                'path_length': 'inf',
                                'path_cost': 'inf',
                            })

                        writer.writerow(result_base)
                        run_id_counter += 1

        print(f"--- Experimento {part_name} concluído. Resultados salvos em {filepath} ---")
