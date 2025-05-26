Abaixo está o conteúdo sugerido para o arquivo `README.md` do projeto **ETL Financeiro com Apache Airflow**, adequado para uso acadêmico ou corporativo em práticas de DataOps.

---

```markdown
# Projeto ETL Financeiro com Apache Airflow

Este projeto implementa um pipeline de ETL orquestrado com Apache Airflow, utilizando Python para coletar, transformar e visualizar dados financeiros da ação PETR4 (Petrobras ON), com base nos princípios de DataOps.

## Objetivos

- Demonstrar o uso de Airflow para orquestração de pipelines de dados.
- Integrar bibliotecas Python para análise financeira automatizada.
- Aplicar práticas de DataOps como versionamento, reprodutibilidade e modularização.
- Expor os alunos à automação de tarefas ETL com agendamento e monitoramento.

---

## Estrutura do Projeto

```

airflow\_custom\_project/
├── dags/
│   └── etl\_financas\_b3.py      # Código da DAG com pipeline ETL
├── Dockerfile                  # Imagem customizada do Airflow com dependências
├── docker-compose.yaml         # Orquestração dos serviços com Docker
├── requirements.txt            # Bibliotecas Python necessárias

````

---

## Descrição da DAG: `etl_financas_b3`

A DAG está agendada para rodar diariamente (`@daily`) e possui três etapas:

1. **extração**:
   - Coleta dados históricos da ação PETR4 usando a API do Yahoo Finance (`yfinance`)
   - Salva como `petr4_raw.csv`

2. **transformação**:
   - Limpa os dados, converte a coluna de fechamento para numérico
   - Calcula a média móvel de 20 dias
   - Salva como `petr4_tratado.csv`

3. **geração de relatório**:
   - Gera gráfico de cotação e média móvel com `matplotlib`
   - Salva como `relatorio_petr4.png`

Os arquivos são gravados nas pastas:

- `dags/data/`: dados extraídos e transformados
- `dags/reports/`: gráfico gerado

---

## Como executar

### 1. Pré-requisitos

- Docker
- Docker Compose

### 2. Instruções

```bash
# Clonar o repositório ou descompactar o .zip
cd airflow_custom_project

# Build da imagem customizada com dependências
docker-compose build

# Subir os containers
docker-compose up -d
````

### 3. Criar usuário no Airflow (primeira execução)

```bash
docker exec -it airflow_web airflow users create --username airflow --firstname Admin --lastname User --role Admin --email admin@example.com --password airflow
```

### 4. Acessar o Airflow

Interface Web: [http://localhost:8088](http://localhost:8088)
Usuário: `airflow`
Senha: `airflow`

---

## Tecnologias Utilizadas

* Apache Airflow 2.8.1
* Python 3.8+
* Pandas
* yfinance
* matplotlib
* Docker e Docker Compose

---

## Licença

Este projeto é de uso acadêmico, livre para reprodução e modificação com finalidade educacional.

