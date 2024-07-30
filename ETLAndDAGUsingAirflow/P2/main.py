# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'matinkzm',  # owner name
    'start_date': days_ago(0),  # start date(in this case today)
    'email': ['matinkzm@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
# define the DAG
dag = DAG(
    dag_id='process_web_log',
    default_args=default_args,
    description='Analyzes the web server log file',
    schedule_interval=timedelta(days=1),
)

# define the tasks
# define the first task (extract)
extract_data = BashOperator(
    task_id='extract_data',
    bash_command='cut -d" " -f1 /home/project/airflow/dags/capstone/accesslog.txt > extracted_data.txt',
    dag=dag,
)

# define the second task (transform)
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='grep -o "198.46.149.143" /home/project/airflow/dags/capstone/extracted_data.txt > transformed_data.txt',
    dag=dag,
)

# define the third task (load)
load_data = BashOperator(
    task_id='load_data',
    bash_command='tar -cvf weblog.tar /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag,
)

# task pipeline
extract_data >> transform_data >> load_data
