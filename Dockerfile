
FROM apache/airflow:2.8.1
COPY requirements.txt /requirements.txt
USER root
RUN pip install --no-cache-dir -r /requirements.txt
USER airflow
