FROM apache/airflow:2.8.1

# Define o usuário airflow para evitar erro com pip
USER airflow

# Copia os requisitos e instala as dependências como usuário airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
