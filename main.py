# -*- coding: utf-8 -*-

"""
Ponto de entrada principal (Main Entry Point) para executar os experimentos do 8-Puzzle.

Este arquivo tem uma única responsabilidade: definir os cenários de teste para
cada parte do experimento e chamar o ExperimentRunner para executá-los.
Funciona como o "painel de controle" do projeto. Para rodar ou pular uma
parte do experimento, basta comentar ou descomentar a chamada correspondente.
"""

# Importa a classe que executa os experimentos.
from runner import ExperimentRunner
# Importa todas as classes de algoritmo do pacote 'algorithms'.
from algorithms import (
    BreadthFirstSearch,
    DepthFirstSearch,
    UniformCostSearch,
    GreedyBestFirstSearch,
    AStarSearch
)


# A função principal que será executada quando o script for chamado.
def main():
    """Define e executa os cenários de teste para o trabalho."""
    # Cria uma instância do ExperimentRunner, que irá gerenciar a criação
    # dos arquivos de resultado na pasta 'results'.
    runner = ExperimentRunner(output_dir="results")

    # Define listas de parâmetros que serão combinados para criar os cenários.
    all_cost_types = ['C1', 'C2', 'C3', 'C4']
    all_heuristics = ['H1', 'H2']

    # --------------------------------------------------------------------------
    # --- Parte 1: Largura vs. Profundidade vs. Custo Uniforme ---
    # --------------------------------------------------------------------------
    print("Definindo cenários da Parte 1...")
    # Inicia uma lista vazia para guardar os cenários da Parte 1.
    part1_scenarios = []
    # Loop pelos algoritmos a serem testados nesta parte.
    for algo in [BreadthFirstSearch, DepthFirstSearch, UniformCostSearch]:
        # Loop pelas funções de custo.
        for cost in all_cost_types:
            # Cria um dicionário para cada combinação e o adiciona à lista de cenários.
            part1_scenarios.append({'algorithm': algo, 'cost_type': cost})
    # Chama o runner para executar os cenários da Parte 1.
    # COMENTE/DESCOMENTE A LINHA ABAIXO PARA RODAR/PULAR ESTE EXPERIMENTO.
    # runner.run_experiment("Part1", part1_scenarios, num_runs=30)

    # --------------------------------------------------------------------------
    # --- Parte 2: Custo Uniforme vs. A* ---
    # --------------------------------------------------------------------------
    print("Definindo cenários da Parte 2...")
    part2_scenarios = []
    for cost in all_cost_types:
        # Adiciona o cenário para a Busca de Custo Uniforme.
        part2_scenarios.append({'algorithm': UniformCostSearch, 'cost_type': cost})
        # Loop pelas heurísticas para criar os cenários da A*.
        for heuristic in all_heuristics:
            part2_scenarios.append({'algorithm': AStarSearch, 'cost_type': cost, 'heuristic': heuristic})
    # Chama o runner para executar os cenários da Parte 2.
    # COMENTE/DESCOMENTE A LINHA ABAIXO PARA RODAR/PULAR ESTE EXPERIMENTO.
    # runner.run_experiment("Part2", part2_scenarios, num_runs=30)

    # --------------------------------------------------------------------------
    # --- Parte 3: Busca Gulosa vs. A* ---
    # --------------------------------------------------------------------------
    print("Definindo cenários da Parte 3...")
    part3_scenarios = []
    # Loop pelas heurísticas para a Busca Gulosa.
    for heuristic in all_heuristics:
        # A Busca Gulosa não usa custo, mas passamos 'C1' como padrão para evitar erros.
        # O custo real será recalculado pelo runner no final.
        part3_scenarios.append({
            'algorithm': GreedyBestFirstSearch,
            'heuristic': heuristic,
            'cost_type': 'C1'
        })
    # Loop para os cenários da A*.
    for cost in all_cost_types:
        for heuristic in all_heuristics:
            part3_scenarios.append({'algorithm': AStarSearch, 'cost_type': cost, 'heuristic': heuristic})
    # Chama o runner para executar os cenários da Parte 3.
    # COMENTE/DESCOMENTE A LINHA ABAIXO PARA RODAR/PULAR ESTE EXPERIMENTO.
    # runner.run_experiment("Part3", part3_scenarios, num_runs=30)

    # --------------------------------------------------------------------------
    # --- Parte 4: Randomização da Vizinhança ---
    # --------------------------------------------------------------------------
    print("Definindo cenários da Parte 4...")
    part4_scenarios = []
    for algo in [BreadthFirstSearch, DepthFirstSearch]:
        for cost in all_cost_types:
            # Cria o cenário ativando a flag 'random_successors' e definindo 10 execuções.
            part4_scenarios.append({
                'algorithm': algo,
                'cost_type': cost,
                'random_successors': True,
                'executions': 10
            })
    # Chama o runner para executar os cenários da Parte 4.
    # COMENTE/DESCOMENTE A LINHA ABAIXO PARA RODAR/PULAR ESTE EXPERIMENTO.
    runner.run_experiment("Part4", part4_scenarios, num_runs=15)

    # Mensagem final para o usuário.
    print("\nTodos os experimentos selecionados foram concluídos.")
    print("Verifique a pasta 'results' para os arquivos CSV gerados.")


# Bloco padrão em Python: se este arquivo for executado diretamente (não importado),
# chama a função main().
if __name__ == '__main__':
    main()
