# -*- coding: utf-8 -*-

"""
Define a classe ExperimentRunner, o "orquestrador" ou "maestro" do projeto.
Sua única responsabilidade é executar os experimentos de forma sistemática,
coletar os dados de desempenho e salvá-los em arquivos CSV para análise posterior.
Ele não contém lógica de busca, apenas gerencia o processo de teste.
"""

# Importa bibliotecas para interagir com o sistema operacional (pastas) e arquivos CSV.
import os
import csv
# Importa a biblioteca 'time' para cronometrar a execução dos algoritmos.
import time
# Importa tipos para anotações.
from typing import List, Dict

# Importa as classes e funções necessárias de outros módulos.
from problem.eight_puzzle import EightPuzzleProblem
from algorithms import GreedyBestFirstSearch
from utils.puzzle_utils import generate_random_state, calculate_path_cost


class ExperimentRunner:
    """Orquestra a execução dos experimentos e salva os resultados em CSV."""

    # O construtor da classe.
    def __init__(self, output_dir="results"):
        # Define o nome do diretório onde os resultados serão salvos.
        self.output_dir = output_dir
        # Verifica se o diretório de saída não existe...
        if not os.path.exists(output_dir):
            # ... e o cria se necessário.
            os.makedirs(output_dir)

    # O método principal que executa uma "parte" do experimento.
    def run_experiment(self, part_name: str, scenarios: List[Dict], num_runs: int):
        # Constrói o caminho completo para o arquivo CSV de resultado.
        filepath = os.path.join(self.output_dir, f"{part_name}_results.csv")
        # Define os cabeçalhos (nomes das colunas) para o arquivo CSV.
        headers = [
            'run_id', 'initial_state', 'algorithm', 'cost_function', 'heuristic', 'random_successors',
            'goal_state_found', 'path_length', 'path_cost', 'nodes_generated', 'nodes_visited', 'execution_time_sec'
        ]

        # Abre o arquivo CSV em modo de escrita ('w').
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            # Cria um "escritor" de CSV que entende o formato de dicionário.
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            # Escreve a linha de cabeçalho no arquivo.
            writer.writeheader()

            # Imprime uma mensagem no console para indicar o início do experimento.
            print(f"\n--- Iniciando Experimento: {part_name} ---")
            # Inicia um contador para identificar cada linha de resultado de forma única.
            run_id_counter = 1

            # Loop principal de execuções: repete 'num_runs' vezes.
            for i in range(num_runs):
                # Gera um novo estado inicial aleatório e solucionável para cada execução.
                initial_state = generate_random_state()
                print(f"  Run {i + 1}/{num_runs} com Estado Inicial: {initial_state}")

                # Loop interno: para cada estado inicial, executa todos os cenários definidos.
                for scenario in scenarios:
                    # Extrai os parâmetros de cada cenário (dicionário).
                    algo_class = scenario['algorithm']
                    cost_type = scenario.get('cost_type')
                    heuristic_type = scenario.get('heuristic')
                    random_succ = scenario.get('random_successors', False)
                    num_executions = scenario.get('executions', 1)  # Para a Parte 4.

                    # Loop de repetições (relevante para a Parte 4).
                    for exec_count in range(num_executions):
                        print(
                            f"    Executando: {algo_class.__name__}, Custo={cost_type or 'N/A'}, Heuristica={heuristic_type or 'N/A'}, Rand={random_succ} ({exec_count + 1}/{num_executions})")

                        # Cria o objeto do problema com os parâmetros do cenário.
                        problem = EightPuzzleProblem(initial_state, cost_type, heuristic_type)
                        # Cria o objeto do algoritmo, passando a flag de randomização.
                        algorithm = algo_class(randomize_successors=random_succ)

                        # Inicia o cronômetro.
                        start_time = time.time()
                        # EXECUTA A BUSCA: Chama o método .search() do algoritmo.
                        solution_node = algorithm.search(problem)
                        # Para o cronômetro.
                        end_time = time.time()

                        # Prepara um dicionário base com os resultados comuns.
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

                        # Se uma solução foi encontrada...
                        if solution_node:
                            path_states = solution_node.get_path()

                            # Tratamento especial para a Busca Gulosa.
                            if algo_class is GreedyBestFirstSearch:
                                # Como a Gulosa não otimiza o custo, calculamos o custo real
                                # para cada uma das 4 funções de custo e escrevemos 4 linhas.
                                for c_type in ['C1', 'C2', 'C3', 'C4']:
                                    recalculated_cost = calculate_path_cost(path_states, c_type)
                                    writer.writerow({**result_base,
                                                     'cost_function': c_type,
                                                     'goal_state_found': str(solution_node.state),
                                                     'path_length': solution_node.depth,
                                                     'path_cost': recalculated_cost,
                                                     })
                                run_id_counter += 1
                                continue  # Pula para a próxima iteração do loop.

                            # Para os outros algoritmos, atualiza o dicionário de resultados.
                            result_base.update({
                                'cost_function': cost_type,
                                'goal_state_found': str(solution_node.state),
                                'path_length': solution_node.depth,
                                'path_cost': solution_node.path_cost,
                            })
                        else:  # Se a busca falhou...
                            # Atualiza o dicionário com valores de falha.
                            result_base.update({
                                'cost_function': cost_type,
                                'goal_state_found': 'None',
                                'path_length': 'inf',
                                'path_cost': 'inf',
                            })

                        # Escreve a linha de resultado no arquivo CSV.
                        writer.writerow(result_base)
                        # Incrementa o contador de ID da execução.
                        run_id_counter += 1

        # Imprime uma mensagem no console para indicar o fim do experimento.
        print(f"--- Experimento {part_name} concluído. Resultados salvos em {filepath} ---")
