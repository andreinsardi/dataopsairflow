# Importações essenciais do Airflow e bibliotecas de processamento
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import yfinance as yf
import os
import matplotlib.pyplot as plt

# Definição dos caminhos onde os arquivos CSV e o gráfico serão salvos
DATA_PATH = '/opt/airflow/dags/data/'
REPORT_PATH = '/opt/airflow/dags/reports/'

# Criação dos diretórios de dados e relatórios, caso não existam
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(REPORT_PATH, exist_ok=True)

# Função de extração: baixa os dados históricos da ação PETR4 do Yahoo Finance
def extrair():
    df = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-31')  # Coleta cotações de 2023
    df.to_csv(f"{DATA_PATH}/petr4_raw.csv")  # Salva em arquivo CSV bruto

# Função de transformação: limpa e processa os dados extraídos
def transformar():
    df = pd.read_csv(f"{DATA_PATH}/petr4_raw.csv", index_col=0)  # Lê o arquivo bruto
    df = df.dropna()  # Remove linhas com valores nulos
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')  # Garante que a coluna 'Close' seja numérica
    df['Media_Movel_20'] = df['Close'].rolling(window=20).mean()  # Calcula a média móvel de 20 dias
    df.to_csv(f"{DATA_PATH}/petr4_tratado.csv")  # Salva o resultado transformado

# Função de geração de relatório: cria e salva um gráfico das cotações e média móvel
def gerar_relatorio():
    df = pd.read_csv(f"{DATA_PATH}/petr4_tratado.csv")  # Lê os dados tratados
    plt.figure(figsize=(10, 6))  # Define o tamanho da figura
    plt.plot(df['Close'], label='Fechamento')  # Plota a série de fechamento
    plt.plot(df['Media_Movel_20'], label='Média Móvel 20 dias')  # Plota a média móvel
    plt.legend()
    plt.title('PETR4 - Fechamento vs Média Móvel')  # Título do gráfico
    plt.savefig(f"{REPORT_PATH}/relatorio_petr4.png")  # Salva o gráfico como imagem

# Argumentos padrão da DAG
default_args = {
    'start_date': datetime(2024, 1, 1),  # Data inicial da DAG
    'catchup': False  # Impede execução retroativa de datas passadas
}

# Definição da DAG principal
with DAG("etl_financas_b3",
         schedule_interval="@daily",  # Executa uma vez por dia
         default_args=default_args,
         description="Pipeline de cotação da PETR4",
         tags=["dataops", "financeiro"]) as dag:

    # Task de extração
    t1 = PythonOperator(
        task_id="extrair_dados",
        python_callable=extrair
    )

    # Task de transformação
    t2 = PythonOperator(
        task_id="transformar_dados",
        python_callable=transformar
    )

    # Task de geração de relatório
    t3 = PythonOperator(
        task_id="gerar_relatorio",
        python_callable=gerar_relatorio
    )

    # Definição da ordem de execução: t1 → t2 → t3
    t1 >> t2 >> t3
