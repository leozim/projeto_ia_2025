# -*- coding: utf-8 -*-

"""
Este script lê os arquivos de resultado .csv da pasta 'results' e gera
gráficos comparativos para análise, salvando-os na pasta 'plots'.

Dependências: pandas, matplotlib, seaborn
Para instalar: pip install pandas matplotlib seaborn
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class ResultPlotter:
    """
    Classe responsável por ler os dados dos experimentos e gerar gráficos.
    """

    def __init__(self, results_dir="results", plots_dir="plots"):
        self.results_dir = results_dir
        self.plots_dir = plots_dir

        if not os.path.exists(self.plots_dir):
            os.makedirs(self.plots_dir)

        # Configurações globais para os gráficos para melhor visualização
        sns.set_theme(style="whitegrid", palette="viridis")
        plt.rcParams['figure.figsize'] = (12, 7)
        plt.rcParams['font.size'] = 12

    def _load_data(self, part_name: str) -> pd.DataFrame | None:
        """Carrega os dados de um arquivo CSV para um DataFrame pandas."""
        filepath = os.path.join(self.results_dir, f"{part_name}_results.csv")
        if not os.path.exists(filepath):
            print(f"Aviso: Arquivo de resultado '{filepath}' não encontrado. Pulando gráficos para esta parte.")
            return None

        df = pd.read_csv(filepath)
        # Converte colunas para numérico, tratando erros. O 'coerce' transforma
        # valores não numéricos (como 'inf') em NaN (Not a Number).
        for col in ['path_cost', 'nodes_visited', 'nodes_generated', 'execution_time_sec']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # CORREÇÃO: A linha abaixo foi removida.
        # df.dropna(inplace=True)
        # Remover a linha acima é a correção principal. Agora, as bibliotecas de plotagem
        # irão simplesmente ignorar os valores NaN ao calcular médias, em vez de
        # apagar linhas inteiras de dados, o que causava o gráfico vazio.

        return df

    def plot_part1(self):
        """Gera gráficos para o Experimento Parte 1."""
        df = self._load_data("Part1")
        if df is None: return

        print("Gerando gráficos para a Parte 1...")

        # Gráfico 1: Custo Médio do Caminho
        plt.figure()
        sns.barplot(data=df, x='cost_function', y='path_cost', hue='algorithm')
        plt.title('Parte 1: Custo Médio do Caminho por Algoritmo e Função de Custo')
        plt.ylabel('Custo Médio do Caminho')
        plt.xlabel('Função de Custo')
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, 'part1_avg_cost.png'))
        plt.close()

        # Gráfico 2: Média de Nós Visitados
        plt.figure()
        sns.barplot(data=df, x='algorithm', y='nodes_visited')
        plt.title('Parte 1: Média de Nós Visitados por Algoritmo')
        plt.ylabel('Média de Nós Visitados (Escala Log)')
        plt.xlabel('Algoritmo')
        plt.yscale('log')  # Escala de log é útil quando os valores variam muito
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, 'part1_avg_nodes.png'))
        plt.close()

    def plot_part2(self):
        """Gera gráficos para o Experimento Parte 2."""
        df = self._load_data("Part2")
        if df is None: return

        print("Gerando gráficos para a Parte 2...")

        df['algorithm_heuristic'] = df.apply(
            lambda row: f"A*({row['heuristic']})" if row['algorithm'] == 'AStarSearch' else 'UCS',
            axis=1
        )

        plt.figure()
        sns.barplot(data=df, x='cost_function', y='nodes_visited', hue='algorithm_heuristic')
        plt.title('Parte 2: Média de Nós Visitados (UCS vs. A*)')
        plt.ylabel('Média de Nós Visitados (Escala Log)')
        plt.xlabel('Função de Custo')
        plt.yscale('log')
        plt.legend(title='Algoritmo (Heurística)')
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, 'part2_nodes_ucs_vs_astar.png'))
        plt.close()

    def plot_part3(self):
        """Gera gráficos para o Experimento Parte 3."""
        df = self._load_data("Part3")
        if df is None: return

        print("Gerando gráficos para a Parte 3...")

        df['algorithm_heuristic'] = df.apply(
            lambda row: f"{row['algorithm'].replace('Search', '')}({row['heuristic']})",
            axis=1
        )

        plt.figure()
        sns.barplot(data=df, x='algorithm_heuristic', y='nodes_visited',
                    order=sorted(df['algorithm_heuristic'].unique()))
        plt.title('Parte 3: Média de Nós Visitados (Greedy vs. A*)')
        plt.ylabel('Média de Nós Visitados (Escala Log)')
        plt.xlabel('Algoritmo (Heurística)')
        plt.xticks(rotation=15)
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, 'part3_avg_nodes_greedy_vs_astar.png'))
        plt.close()

        plt.figure()
        sns.barplot(data=df, x='algorithm_heuristic', y='path_cost', hue='cost_function',
                    order=sorted(df['algorithm_heuristic'].unique()))
        plt.title('Parte 3: Custo Médio do Caminho (Greedy vs. A*)')
        plt.ylabel('Custo Médio do Caminho')
        plt.xlabel('Algoritmo (Heurística)')
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, 'part3_avg_cost_greedy_vs_astar.png'))
        plt.close()

    def plot_all(self):
        """Chama todas as funções de plotagem."""
        print("Iniciando geração de todos os gráficos...")
        self.plot_part1()
        self.plot_part2()
        self.plot_part3()
        print("\nGeração de gráficos concluída. Verifique a pasta 'plots'.")


if __name__ == '__main__':
    plotter = ResultPlotter()
    plotter.plot_all()
